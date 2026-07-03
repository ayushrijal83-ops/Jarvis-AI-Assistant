# gesture.py
from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Optional, Tuple

import cv2
import mediapipe as mp

from utils import UiEvent


@dataclass
class GestureConfig:
    camera_index: int = 0
    max_num_hands: int = 1
    min_detection_confidence: float = 0.6
    min_tracking_confidence: float = 0.6
    fps_limit: float = 24.0  # keep CPU stable

    # Debug preview
    debug_preview: bool = False
    preview_window_name: str = "Jarvis Gesture Debug"


class GestureManager:
    """
    Camera SINGLE SOURCE:
    - Owns the webcam (ONLY module opening it)
    - Detects hand gestures
    - Stores latest frame for other modules (Vision)
    """

    def __init__(self, event_q, cfg: Optional[GestureConfig] = None):
        self.event_q = event_q
        self.cfg = cfg or GestureConfig()

        self._stop = threading.Event()
        self._thread: Optional[threading.Thread] = None

        # Latest gesture text
        self._latest_label = "—"
        self._latest_ts = 0.0
        self._latest_lock = threading.Lock()

        # Latest frame (BGR)
        self._frame = None
        self._frame_ts = 0.0
        self._frame_lock = threading.Lock()

        # Emit throttling
        self._last_emit_ts = 0.0
        self._emit_interval = 0.12

    def start(self):
        self._stop.clear()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        self._ui_log("[system] GestureManager started (camera).")

    def stop(self):
        self._stop.set()
        self._ui_log("[system] GestureManager stopping...")

    # ---------- UI helpers ----------
    def _ui_log(self, text: str):
        self.event_q.put(UiEvent(type="log", payload={"text": text}))

    def _ui_gesture(self, label: str):
        now = time.time()
        if label == self._latest_label and (now - self._last_emit_ts) < self._emit_interval:
            return
        self._last_emit_ts = now
        self.event_q.put(UiEvent(type="gesture", payload={"text": label}))

    # ---------- External getters ----------
    def get_latest(self) -> Tuple[str, float]:
        with self._latest_lock:
            return self._latest_label, self._latest_ts

    def get_latest_frame(self):
        """
        Returns (frame_copy, timestamp).
        frame is BGR numpy array or None.
        """
        with self._frame_lock:
            if self._frame is None:
                return None, 0.0
            return self._frame.copy(), self._frame_ts

    # ---------- main loop ----------
    def _loop(self):
        cap = cv2.VideoCapture(self.cfg.camera_index, cv2.CAP_DSHOW)
        if not cap.isOpened():
            self._ui_log("[error] Camera not available for GestureManager.")
            with self._latest_lock:
                self._latest_label = "CAMERA ERROR"
                self._latest_ts = time.time()
            self._ui_gesture("CAMERA ERROR")
            return

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=self.cfg.max_num_hands,
            min_detection_confidence=self.cfg.min_detection_confidence,
            min_tracking_confidence=self.cfg.min_tracking_confidence,
        )

        target_dt = 1.0 / max(1.0, float(self.cfg.fps_limit))
        last_frame_ts = 0.0

        try:
            while not self._stop.is_set():
                now = time.time()
                if now - last_frame_ts < target_dt:
                    time.sleep(0.002)
                    continue
                last_frame_ts = now

                ok, frame = cap.read()
                if not ok or frame is None:
                    self._set_gesture("NO FRAME")
                    self._ui_gesture("NO FRAME")
                    continue

                # Save latest frame for Vision (single source)
                with self._frame_lock:
                    self._frame = frame
                    self._frame_ts = time.time()

                if self.cfg.debug_preview:
                    cv2.imshow(self.cfg.preview_window_name, frame)
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break

                # Gesture detection
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                res = hands.process(rgb)

                label = "—"
                if res.multi_hand_landmarks:
                    lm = res.multi_hand_landmarks[0].landmark
                    label = self._classify(lm)

                self._set_gesture(label)
                self._ui_gesture(label)

        except Exception as e:
            self._ui_log(f"[error] Gesture loop crashed: {e}")
            self._set_gesture("GESTURE ERROR")
            self._ui_gesture("GESTURE ERROR")
        finally:
            try:
                hands.close()
            except Exception:
                pass
            cap.release()
            if self.cfg.debug_preview:
                try:
                    cv2.destroyAllWindows()
                except Exception:
                    pass

    def _set_gesture(self, label: str):
        with self._latest_lock:
            self._latest_label = label
            self._latest_ts = time.time()

    def _classify(self, lm) -> str:
        wrist = lm[0]
        index_mcp = lm[5]
        pinky_mcp = lm[17]
        tips = [lm[4], lm[8], lm[12], lm[16], lm[20]]

        cx = (wrist.x + index_mcp.x + pinky_mcp.x) / 3.0
        cy = (wrist.y + index_mcp.y + pinky_mcp.y) / 3.0

        d = 0.0
        for t in tips:
            dx = t.x - cx
            dy = t.y - cy
            d += (dx * dx + dy * dy) ** 0.5
        d /= len(tips)

        if d < 0.16:
            return "FIST"
        if d > 0.23:
            tilt = index_mcp.x - pinky_mcp.x
            if tilt < -0.08:
                return "LEFT"
            if tilt > 0.08:
                return "RIGHT"
            return "PALM"
        return "HAND"
