# vision.py
from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Optional

import cv2
import mediapipe as mp
import numpy as np

from utils import UiEvent


@dataclass
class VisionConfig:
    # Face presence
    min_face_confidence: float = 0.3
    face_lost_timeout_s: float = 1.0

    # Eyes (EAR)
    eye_closed_threshold: float = 0.20
    drowsy_time_s: float = 1.8

    # Head / attention thresholds (tune later)
    yaw_thresh: float = 0.16      # left/right looking away
    pitch_down_thresh: float = 0.10
    pitch_up_thresh: float = -0.10
    roll_thresh_deg: float = 12.0

    poll_dt: float = 0.05

    debug_preview: bool = False
    preview_window_name: str = "Jarvis Vision Debug"


class VisionManager:
    """
    Phase 6.3:
    - Uses frames from GestureManager (single camera owner)
    - Face presence detection
    - Eyes open/closed + drowsy (EAR)
    - Head tilt + attention (yaw/pitch/roll heuristic)
    Emits states:
      FACE DETECTED / FACE LOST
      EYES OPEN / EYES CLOSED / DROWSY
      ATTENTIVE / DISTRACTED
      HEAD LEFT / HEAD RIGHT
      LOOKING DOWN / LOOKING UP
    """

    def __init__(self, event_q, gesture_manager, cfg: Optional[VisionConfig] = None):
        self.event_q = event_q
        self.gm = gesture_manager
        self.cfg = cfg or VisionConfig()

        self._stop = threading.Event()
        self._thread: Optional[threading.Thread] = None

        self._face_present = False
        self._last_face_ts = 0.0

        self._eye_state = "UNKNOWN"
        self._eyes_closed_ts = 0.0

        self._attention_state = "UNKNOWN"
        self._head_state = "NEUTRAL"
        self._pitch_state = "NEUTRAL"

        self._mp_face = mp.solutions.face_detection.FaceDetection(
            model_selection=0,
            min_detection_confidence=self.cfg.min_face_confidence,
        )

        self._mp_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=False,
            refine_landmarks=True,
            max_num_faces=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        self._attention_ok = True
        self._paused_by_attention = False


    # ---------- lifecycle ----------
    def start(self):
        self._stop.clear()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        self._log("[system] VisionManager started (face + eyes + attention).")

    def stop(self):
        self._stop.set()
        self._log("[system] VisionManager stopping...")

    # ---------- UI helpers ----------
    def _log(self, text: str):
        self.event_q.put(UiEvent(type="log", payload={"text": text}))

    def _state(self, state: str):
        self.event_q.put(UiEvent(type="state", payload={"state": state, "log": None}))

    def _set_state_once(self, attr_name: str, new_value: str, emit_state: str):
        cur = getattr(self, attr_name)
        if cur != new_value:
            setattr(self, attr_name, new_value)
            self._state(emit_state)

    # ---------- eye math ----------
    def _eye_aspect_ratio(self, eye_pts):
        A = np.linalg.norm(eye_pts[1] - eye_pts[5])
        B = np.linalg.norm(eye_pts[2] - eye_pts[4])
        C = np.linalg.norm(eye_pts[0] - eye_pts[3])
        return (A + B) / (2.0 * C + 1e-6)

    # ---------- head + attention ----------
    def _compute_head_signals(self, lm, w: int, h: int):
        """
        Returns:
          yaw_norm: nose_x relative to eye center (normalized to inter-eye distance)
          pitch_norm: nose_y relative to eye-line y (normalized to face height proxy)
          roll_deg: eye-line slope in degrees
        """
        # Key landmarks
        NOSE_TIP = 1
        LEFT_EYE_OUTER = 33
        RIGHT_EYE_OUTER = 263
        LEFT_CHEEK = 234
        RIGHT_CHEEK = 454

        nose = lm[NOSE_TIP]
        le = lm[LEFT_EYE_OUTER]
        re = lm[RIGHT_EYE_OUTER]
        lc = lm[LEFT_CHEEK]
        rc = lm[RIGHT_CHEEK]

        nose_xy = np.array([nose.x * w, nose.y * h])
        le_xy = np.array([le.x * w, le.y * h])
        re_xy = np.array([re.x * w, re.y * h])

        eye_center = (le_xy + re_xy) / 2.0
        inter_eye = np.linalg.norm(le_xy - re_xy) + 1e-6

        # Yaw: nose x offset vs eye center normalized by inter-eye distance
        yaw_norm = (nose_xy[0] - eye_center[0]) / inter_eye

        # Roll: slope of eye line
        dy = (re_xy[1] - le_xy[1])
        dx = (re_xy[0] - le_xy[0]) + 1e-6
        roll_rad = np.arctan2(dy, dx)
        roll_deg = float(np.degrees(roll_rad))

        # Pitch proxy: nose y vs eye-line y, normalize by face width proxy
        lc_xy = np.array([lc.x * w, lc.y * h])
        rc_xy = np.array([rc.x * w, rc.y * h])
        face_width = np.linalg.norm(lc_xy - rc_xy) + 1e-6

        pitch_norm = (nose_xy[1] - eye_center[1]) / face_width

        return yaw_norm, pitch_norm, roll_deg

    # ---------- main loop ----------
    def _loop(self):
        last_frame_ts_seen = 0.0

        # Eye landmark indices (MediaPipe)
        LEFT_EYE = [33, 160, 158, 133, 153, 144]
        RIGHT_EYE = [362, 385, 387, 263, 373, 380]

        try:
            while not self._stop.is_set():
                frame, ts = self.gm.get_latest_frame()

                if frame is None or ts == 0.0 or ts == last_frame_ts_seen:
                    time.sleep(self.cfg.poll_dt)
                    continue

                last_frame_ts_seen = ts

                if self.cfg.debug_preview:
                    cv2.imshow(self.cfg.preview_window_name, frame)
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break

                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face_res = self._mp_face.process(rgb)

                now = time.time()

                # ---------- FACE PRESENCE ----------
                if face_res.detections:
                    self._last_face_ts = now
                    if not self._face_present:
                        self._face_present = True
                        self._state("FACE DETECTED")
                else:
                    if self._face_present and (now - self._last_face_ts) > self.cfg.face_lost_timeout_s:
                        self._face_present = False
                        self._state("FACE LOST")
                        self._eye_state = "UNKNOWN"
                        self._attention_state = "UNKNOWN"
                        self._head_state = "NEUTRAL"
                        self._pitch_state = "NEUTRAL"
                    time.sleep(self.cfg.poll_dt)
                    continue

                # ---------- FACEMESH ----------
                mesh_res = self._mp_mesh.process(rgb)
                if not mesh_res.multi_face_landmarks:
                    time.sleep(self.cfg.poll_dt)
                    continue

                h, w, _ = frame.shape
                lm = mesh_res.multi_face_landmarks[0].landmark

                # ---------- EYES (EAR) ----------
                left_eye = np.array([(lm[i].x * w, lm[i].y * h) for i in LEFT_EYE])
                right_eye = np.array([(lm[i].x * w, lm[i].y * h) for i in RIGHT_EYE])

                ear = (self._eye_aspect_ratio(left_eye) + self._eye_aspect_ratio(right_eye)) / 2.0

                if ear < self.cfg.eye_closed_threshold:
                    if self._eye_state != "EYES CLOSED":
                        self._eye_state = "EYES CLOSED"
                        self._eyes_closed_ts = now
                        self._state("EYES CLOSED")
                    else:
                        if (now - self._eyes_closed_ts) > self.cfg.drowsy_time_s and self._eye_state != "DROWSY":
                            self._eye_state = "DROWSY"
                            self._state("DROWSY")
                else:
                    if self._eye_state != "EYES OPEN":
                        self._eye_state = "EYES OPEN"
                        self._state("EYES OPEN")

                # ---------- HEAD + ATTENTION ----------
                yaw_norm, pitch_norm, roll_deg = self._compute_head_signals(lm, w, h)

                # Attention (looking away)
                if abs(yaw_norm) > self.cfg.yaw_thresh:
                    self._set_state_once("_attention_state", "DISTRACTED", "DISTRACTED")
                else:
                    self._set_state_once("_attention_state", "ATTENTIVE", "ATTENTIVE")

                # Head LEFT/RIGHT (roll)
                if roll_deg > self.cfg.roll_thresh_deg:
                    self._set_state_once("_head_state", "HEAD RIGHT", "HEAD RIGHT")
                elif roll_deg < -self.cfg.roll_thresh_deg:
                    self._set_state_once("_head_state", "HEAD LEFT", "HEAD LEFT")
                else:
                    self._set_state_once("_head_state", "NEUTRAL", "HEAD NEUTRAL")

                # Looking UP/DOWN (pitch proxy)
                if pitch_norm > self.cfg.pitch_down_thresh:
                    self._set_state_once("_pitch_state", "DOWN", "LOOKING DOWN")
                elif pitch_norm < self.cfg.pitch_up_thresh:
                    self._set_state_once("_pitch_state", "UP", "LOOKING UP")
                else:
                    self._set_state_once("_pitch_state", "NEUTRAL", "LOOKING CENTER")

                time.sleep(self.cfg.poll_dt)

        except Exception as e:
            self._log(f"[error] Vision crashed: {e}")
            self._state("ERROR")

        finally:
            if self.cfg.debug_preview:
                cv2.destroyAllWindows()
            try:
                self._mp_face.close()
            except Exception:
                pass
            try:
                self._mp_mesh.close()
            except Exception:
                pass
            self._log("[system] VisionManager stopped.")
    def on_vision_state(self, state: str):
        """
        Called when VisionManager emits a state.
        """
        if state in ("DISTRACTED", "LOOKING DOWN"):
            self._attention_ok = False
            if self._is_speaking.is_set():
                self._paused_by_attention = True
                self._tts_interrupt.set()

        elif state in ("ATTENTIVE", "LOOKING CENTER"):
            self._attention_ok = True
            # Resume only if we paused it
            if self._paused_by_attention:
                self._paused_by_attention = False
