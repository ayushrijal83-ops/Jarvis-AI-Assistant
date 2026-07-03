# game_mode.py
import time
import pyautogui

from config import GAME_KEYMAP, INPUT_RATE_LIMIT_S                           

class GameController:
    def __init__(self):
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0
        self._last_ts = 0.0
        self._held = set()  # keys currently held down

    def _rate_limit(self):
        now = time.time()
        if now - self._last_ts < INPUT_RATE_LIMIT_S:
            return False
        self._last_ts = now
        return True

    def tap(self, key: str):
        if not self._rate_limit():
            return False, "Too fast."
        try:
            pyautogui.press(key)
            return True, f"Tapped {key}"
        except Exception as e:
            return False, f"Tap failed: {e}"

    def hold(self, key: str):
        # Holding should not be rate-limited too aggressively; only act on change.
        try:
            if key in self._held:
                return True, "Already holding"
            pyautogui.keyDown(key)
            self._held.add(key)
            return True, f"Holding {key}"
        except Exception as e:
            return False, f"Hold failed: {e}"

    def release(self, key: str):
        try:
            if key not in self._held:
                return True, "Not held"
            pyautogui.keyUp(key)
            self._held.discard(key)
            return True, f"Released {key}"
        except Exception as e:
            return False, f"Release failed: {e}"

    def stop_all(self):
        # Release anything we might be holding
        try:
            for k in list(self._held):
                pyautogui.keyUp(k)
            self._held.clear()
            return True, "Stopped"
        except Exception as e:
            return False, f"Stop failed: {e}"

    # Voice command still supported
    def execute(self, command: str):
        cmd = command.lower().strip()
        key = GAME_KEYMAP.get(cmd)
        if not key:
            return False, f"Unknown game command: {cmd}"
        return self.tap(key)
