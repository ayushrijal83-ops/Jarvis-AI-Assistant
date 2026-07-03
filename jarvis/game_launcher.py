# game_launcher.py
from __future__ import annotations

import subprocess
from pathlib import Path

try:
    import psutil
except Exception:
    psutil = None

from utils import UiEvent
from config import (
    AUTO_LAUNCH_GAME_ON_GAME_MODE,
    GAME_EXE_PATH,
    GAME_WORKING_DIR,
    GAME_PROCESS_NAME,
    GAME_STEAM_URI,   # used for Steam OR Microsoft Store shell URI
)


# -------------------------------------------------
# Helper: check if process already running
# -------------------------------------------------
def _is_running_process(name: str) -> bool:
    name = (name or "").lower().strip()
    if not name or not psutil:
        return False

    for p in psutil.process_iter(["name"]):
        try:
            if (p.info["name"] or "").lower() == name:
                return True
        except Exception:
            continue
    return False


# -------------------------------------------------
# Main launcher
# -------------------------------------------------
def launch_game_if_needed(event_q=None) -> tuple[bool, str]:
    """
    Launch game when GAME MODE is enabled.

    Supports:
    1) Normal EXE games
    2) Steam games (steam://run/ID)
    3) Microsoft Store games (shell:AppsFolder\\APP_ID)

    Returns:
        (success: bool, message: str)
    """

    if not AUTO_LAUNCH_GAME_ON_GAME_MODE:
        return True, "Auto-launch disabled."

    # If game already running, do nothing
    if GAME_PROCESS_NAME and _is_running_process(GAME_PROCESS_NAME):
        return True, "Game already running."

    # -------------------------------------------------
    # 1) Direct EXE launch (BEST if available)
    # -------------------------------------------------
    if GAME_EXE_PATH:
        exe = Path(GAME_EXE_PATH)
        if exe.exists():
            try:
                cwd = str(Path(GAME_WORKING_DIR)) if GAME_WORKING_DIR else str(exe.parent)
                subprocess.Popen(
                    [str(exe)],
                    cwd=cwd,
                    shell=False
                )
                if event_q:
                    event_q.put(UiEvent("log", {"text": "[system] Game launched (EXE)."}))
                return True, "Launching game."
            except Exception as e:
                return False, f"Failed to launch EXE game: {e}"

    # -------------------------------------------------
    # 2) Steam / Microsoft Store app launch
    # (IMPORTANT: use explorer.exe, NOT os.startfile)
    # -------------------------------------------------
    if GAME_STEAM_URI:
        try:
            subprocess.Popen(
                ["explorer.exe", GAME_STEAM_URI],
                shell=False
            )
            if event_q:
                event_q.put(UiEvent("log", {"text": "[system] Game launched (Store / Steam)."}))
            return True, "Launching game."
        except Exception as e:
            return False, f"Failed to launch Store/Steam game: {e}"

    # -------------------------------------------------
    # Nothing configured
    # -------------------------------------------------
    return (
        False,
        "Game launch not configured. Set GAME_EXE_PATH or GAME_STEAM_URI in config.py."
    )
