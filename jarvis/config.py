# config.py
APP_TITLE = "JARVIS Assistant"
BG = "#050B14"
ACCENT = "#00E5FF"      # neon cyan
ACCENT_DIM = "#007A8A"  # dim cyan
TEXT = "#D7F9FF"
ERROR = "#FF3B3B"

WIN_W = 980
WIN_H = 620

FPS_MS = 16  # ~60fps UI tick

# Core animation sizing
CORE_RADIUS = 90
RING_GAP = 16
RING_COUNT = 3

# UI layout
LOG_LINES_MAX = 200

# Modes
MODES = ("AI", "PC", "GAME")

MODE_COLORS = {
    "AI": "#00E5FF",     # cyan
    "PC": "#4DFF88",     # green
    "GAME": "#FF8C42",   # orange
}

# ---- Voice (Phase 2) ----
from pathlib import Path

WAKE_WORD = "jarvis"

# Path: jarvis_assistant/models/vosk/vosk-model-small-en-us-0.15
VOSK_MODEL_PATH = Path(__file__).resolve().parent / "models" / "vosk" / "vosk-model-en-us-0.22"

SAMPLE_RATE = 16000
CHANNELS = 1

# If sounddevice picks the wrong mic, set this to an integer device index (see testing section)
INPUT_DEVICE = None  # e.g. 1 or 2

# ---- AI Memory (Step 3.2) ----
MEMORY_MAX_TURNS = 8  # user+assistant pairs kept in RAM (safe default)

# ---- PC Control (Phase 4) ----

APP_WHITELIST = {
    "chrome": {
        "windows": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "linux": "google-chrome",
    },
    "notepad": {
        "windows": "notepad.exe",
        "linux": "gedit",
    },
    "calculator": {
        "windows": "calc.exe",
        "linux": "gnome-calculator",
    },
}

# ---- Voice cancel / barge-in ----
CANCEL_PHRASES = ["jarvis stop", "jarvis cancel", "stop", "cancel"]
REQUIRE_WAKE_FOR_CANCEL = True   # recommended: avoids Jarvis hearing itself

# ---- Input Control Safety (Step 4.3) ----
PYAUTOGUI_FAILSAFE = True          # move mouse to top-left to abort
PYAUTOGUI_PAUSE = 0.08             # small pause between actions
INPUT_RATE_LIMIT_S = 0.35          # prevent accidental spam
TYPE_MAX_CHARS = 120               # prevent huge typing accidents

ALLOWED_KEYS = {
    "enter": "enter",
    "esc": "esc",
    "escape": "esc",
    "tab": "tab",
    "backspace": "backspace",
    "space": "space",
}


# ---- Hotkeys (Step 4.3.3) ----
ALLOWED_HOTKEYS = {
    "copy": ["ctrl", "c"],
    "paste": ["ctrl", "v"],
    "select all": ["ctrl", "a"],
    "alt tab": ["alt", "tab"],
    "close window": ["alt", "f4"],  # risky -> confirm
}

RISKY_HOTKEYS = {"close window"}
CONFIRM_WINDOW_S = 5.0


# ---- GAME MODE ----
GAME_MODE_DEFAULT = False

GAME_KEYMAP = {
    "left": "a",
    "right": "d",
    "jump": "space",
    "fire": "f",
    "shoot": "f",
    "reload": "r",
}

# ---- Whisper ASR (Hybrid) ----
WHISPER_MODEL_SIZE = "small"   # try: "base" if your CPU is slow; "small" is a good default
WHISPER_DEVICE = "cuda"         # later: "cuda"
WHISPER_COMPUTE_TYPE = "float16"  # cpu default
WHISPER_MAX_SECONDS = 4.0     # record only a short command clip after wake word
# ---- Whisper capture tuning ----
WHISPER_MIN_SECONDS = 3      # minimum command capture
WHISPER_SILENCE_MS = 450       # stop after this much silence
WHISPER_ENERGY_THRESH = 400    # tweak 250–800 depending on mic

# ---- Demo Mode ----
DEMO_ENABLED = True
DEMO_IDLE_SECONDS = 12        # start demo after X seconds of inactivity
DEMO_MESSAGE_EVERY = 6        # post a system line every X seconds while demo active

# ---- Game auto-launch (Microsoft Store app) ----
AUTO_LAUNCH_GAME_ON_GAME_MODE = True

GAME_EXE_PATH = ""
GAME_WORKING_DIR = ""
GAME_PROCESS_NAME = ""

# Microsoft Store App ID
GAME_APP_ID = "VectorUnit.BeachBuggyRacing_hvbhrz8672s2!App"
GAME_STEAM_URI = rf"shell:AppsFolder\{GAME_APP_ID}"
