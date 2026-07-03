# control.py
from __future__ import annotations

import os
import subprocess
import sys

from config import APP_WHITELIST

import time
import pyautogui

from config import (
    PYAUTOGUI_FAILSAFE, PYAUTOGUI_PAUSE,
    INPUT_RATE_LIMIT_S, TYPE_MAX_CHARS, ALLOWED_KEYS
)



class PCController:
    """
    SAFE PC controller.
    - Only opens whitelisted apps
    - No destructive actions
    """
    def search_web(self, query: str) -> tuple[bool, str]:
        if not query:
            return False, "What should I search for?"

        import webbrowser
        import urllib.parse

        q = urllib.parse.quote_plus(query)
        url = f"https://www.google.com/search?q={q}"

        try:
            webbrowser.open(url)
            return True, f"Searching for {query}."
        except Exception as e:
            return False, f"Search failed: {e}"


    def __init__(self):
        self.platform = "windows" if sys.platform.startswith("win") else "linux"
        pyautogui.FAILSAFE = PYAUTOGUI_FAILSAFE
        pyautogui.PAUSE = PYAUTOGUI_PAUSE
        self.last_input_ts = 0.0

    def list_apps(self) -> list[str]:
        return list(APP_WHITELIST.keys())

    def open_app(self, app_name: str) -> tuple[bool, str]:
        app = app_name.lower().strip()

        if app not in APP_WHITELIST:
            return False, f"I am not allowed to open {app}."

        cmd = APP_WHITELIST[app].get(self.platform)

        if not cmd:
            return False, f"{app} is not configured for {self.platform}."

        try:
            if self.platform == "windows":
                subprocess.Popen(cmd, shell=True)
            else:
                subprocess.Popen([cmd])

            return True, f"Opening {app}."

        except Exception as e:
            return False, f"Failed to open {app}: {e}"
        

    def _rate_limit(self) -> tuple[bool, str]:
        now = time.time()
        if (now - self._last_input_ts) < INPUT_RATE_LIMIT_S:
            return False, "Too fast. Try again."
        self._last_input_ts = now
        return True, ""

    def click(self) -> tuple[bool, str]:
        ok, msg = self._rate_limit()
        if not ok:
            return False, msg
        try:
            pyautogui.click()
            return True, "Clicked."
        except Exception as e:
            return False, f"Click failed: {e}"

    def double_click(self) -> tuple[bool, str]:
        ok, msg = self._rate_limit()
        if not ok:
            return False, msg
        try:
            pyautogui.doubleClick()
            return True, "Double clicked."
        except Exception as e:
            return False, f"Double click failed: {e}"

    def scroll(self, direction: str, amount: int = 450) -> tuple[bool, str]:
        ok, msg = self._rate_limit()
        if not ok:
            return False, msg

        direction = (direction or "").lower()
        amt = max(50, min(int(amount), 2000))  # clamp

        try:
            if direction in ("down", "scroll down"):
                pyautogui.scroll(-amt)
                return True, "Scrolled down."
            elif direction in ("up", "scroll up"):
                pyautogui.scroll(amt)
                return True, "Scrolled up."
            else:
                return False, "Say scroll up or scroll down."
        except Exception as e:
            return False, f"Scroll failed: {e}"

    def type_text(self, text: str) -> tuple[bool, str]:
        ok, msg = self._rate_limit()
        if not ok:
            return False, msg

        text = (text or "").strip()
        if not text:
            return False, "What should I type?"

        if len(text) > TYPE_MAX_CHARS:
            text = text[:TYPE_MAX_CHARS]

        try:
            pyautogui.write(text, interval=0.01)
            return True, "Typed."
        except Exception as e:
            return False, f"Typing failed: {e}"

    def press_key(self, key_name: str) -> tuple[bool, str]:
        ok, msg = self._rate_limit()
        if not ok:
            return False, msg

        k = (key_name or "").strip().lower()
        k = ALLOWED_KEYS.get(k)
        if not k:
            allowed = ", ".join(sorted(ALLOWED_KEYS.keys()))
            return False, f"Key not allowed. Allowed: {allowed}"

        try:
            pyautogui.press(k)
            return True, f"Pressed {k}."
        except Exception as e:
            return False, f"Key press failed: {e}"
        
    def hotkey(self, name: str) -> tuple[bool, str]:
        ok, msg = self._rate_limit()
        if not ok:
            return False, msg

        from config import ALLOWED_HOTKEYS

        n = (name or "").strip().lower()
        combo = ALLOWED_HOTKEYS.get(n)
        if not combo:
            allowed = ", ".join(sorted(ALLOWED_HOTKEYS.keys()))
            return False, f"Hotkey not allowed. Allowed: {allowed}"

        try:
            import pyautogui
            pyautogui.hotkey(*combo)
            return True, f"Done: {n}."
        except Exception as e:
            return False, f"Hotkey failed: {e}"

    