# gesture_control.py
from __future__ import annotations

import threading
import time
from collections import deque

from shared_state import is_game_mode
from game_mode import GameController
from game_profiles import BEACH_BUGGY_RACING
from utils import UiEvent


PROFILE = BEACH_BUGGY_RACING


class GestureGameDriver:
    """
    Gesture -> Beach Buggy Racing control (Phase 5.3)

    Gestures (from gesture.py):
      LEFT  -> hold A
      RIGHT -> hold D
      PALM/HAND -> hold W (accelerate)
      FIST  -> tap SPACE (power-up)
      NO HAND / errors -> stop_all (release keys)

    Only sends input when is_game_mode() == True.
    Includes smoothing + safety timeouts.
    """

    def __init__(self, gesture_manager, event_q):
        self.gm = gesture_manager
        self.event_q = event_q

        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

        self.gc = GameController()

        # Smoothing window (majority vote)
        self._hist = deque(maxlen=7)  # slightly bigger for racing stability

        # State tracking
        self._last_action = "STOP"

        # Fist debounce
        self._last_fist_ts = 0.0
        self._fist_cooldown = 0.70  # power-up should not spam

        # Safety: if hand disappears, stop
        self._nohand_timeout = 0.55

        # Poll rate (lower = more CPU, higher = less responsive)
        self._poll_dt = 0.03  # ~33 fps

    def start(self):
        self._stop.clear()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        self._log(f"[system] GestureGameDriver started ({PROFILE.get('name','profile')}).")

    def stop(self):
        self._stop.set()
        try:
            self.gc.stop_all()
        except Exception:
            pass
        self._log("[system] GestureGameDriver stopped.")

    def _log(self, text: str):
        self.event_q.put(UiEvent(type="log", payload={"text": text}))

    def _loop(self):
        while not self._stop.is_set():
            time.sleep(self._poll_dt)

            # If game mode is off, release anything held and idle
            if not is_game_mode():
                if self._last_action != "STOP":
                    self.gc.stop_all()
                    self._last_action = "STOP"
                self._hist.clear()
                continue

            label, ts = self.gm.get_latest()

            # Safety: camera errors or no updates => stop
            if (
                label in ("—", "NO FRAME", "CAMERA ERROR", "GESTURE ERROR")
                or (time.time() - ts) > self._nohand_timeout
            ):
                self._safe_stop()
                continue

            # Smoothing
            self._hist.append(label)
            stable = self._majority(self._hist)

            # Routing for Beach Buggy:
            # LEFT / RIGHT steering
            if stable == "LEFT":
                self._move("LEFT")
                continue

            if stable == "RIGHT":
                self._move("RIGHT")
                continue

            # PALM/HAND = accelerate forward
            if stable in ("PALM", "HAND"):
                self._move("FORWARD")
                continue

            # FIST = power-up (tap)
            if stable == "FIST":
                self._fire()
                # Keep whatever last movement was (don’t force stop)
                continue

            # Unknown => stop
            self._safe_stop()

    def _majority(self, items):
        counts = {}
        for x in items:
            counts[x] = counts.get(x, 0) + 1
        return max(counts, key=counts.get)

    def _safe_stop(self):
        if self._last_action != "STOP":
            self.gc.stop_all()
            self._last_action = "STOP"
        self._hist.clear()

    def _move(self, action: str):
        """
        action in: LEFT, RIGHT, FORWARD, STOP
        Holds only the needed keys; releases previous held movement.
        """
        if action == self._last_action:
            return

        # Release previous movement
        if self._last_action == "LEFT":
            self.gc.release(PROFILE["left"])
        elif self._last_action == "RIGHT":
            self.gc.release(PROFILE["right"])
        elif self._last_action == "FORWARD":
            self.gc.release(PROFILE["accelerate"])

        # Apply new movement
        if action == "LEFT":
            self.gc.hold(PROFILE["left"])
        elif action == "RIGHT":
            self.gc.hold(PROFILE["right"])
        elif action == "FORWARD":
            self.gc.hold(PROFILE["accelerate"])
        else:
            self.gc.stop_all()

        self._last_action = action

    def _fire(self):
        now = time.time()
        if now - self._last_fist_ts < self._fist_cooldown:
            return
        self._last_fist_ts = now
        self.gc.tap(PROFILE["fire"])
