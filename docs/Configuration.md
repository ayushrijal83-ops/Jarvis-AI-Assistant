# ⚙️ Configuration Guide

## Introduction

The `config.py` file is the central configuration file for the **Jarvis AI Assistant**.

Instead of hardcoding values throughout the project, all major settings are stored in one place, making the assistant easy to customize without modifying the core source code.

This document explains every configurable option, its purpose, recommended values, and any safety considerations.

---

# Configuration Categories

The configuration file is divided into the following sections:

* User Interface
* Voice Recognition
* AI Memory
* Desktop Automation
* Safety Controls
* Keyboard & Mouse
* Game Mode
* Whisper Speech Recognition
* Demo Mode
* Game Launcher

---

# User Interface Settings

These options control the appearance and layout of the graphical interface.

## APP_TITLE

```python
APP_TITLE = "JARVIS Assistant"
```

**Purpose**

The title displayed in the application window.

**Example**

```
JARVIS Assistant
```

---

## Background Color

```python
BG = "#050B14"
```

Dark background color used throughout the interface.

---

## Accent Color

```python
ACCENT = "#00E5FF"
```

Primary highlight color used for buttons, indicators, and animations.

---

## Dim Accent

```python
ACCENT_DIM = "#007A8A"
```

A darker version of the accent color used for inactive UI elements.

---

## Text Color

```python
TEXT = "#D7F9FF"
```

Primary text color.

---

## Error Color

```python
ERROR = "#FF3B3B"
```

Used for warning and error messages.

---

## Window Size

```python
WIN_W = 980
WIN_H = 620
```

Specifies the default application window size.

---

## FPS_MS

```python
FPS_MS = 16
```

Controls the UI refresh interval.

16 ms ≈ 60 FPS.

---

# Core Animation

These values define the animated assistant core displayed in the interface.

## CORE_RADIUS

```python
CORE_RADIUS = 90
```

Radius of the animated center element.

---

## RING_GAP

```python
RING_GAP = 16
```

Spacing between animated rings.

---

## RING_COUNT

```python
RING_COUNT = 3
```

Number of animated rings.

---

# Log Settings

## LOG_LINES_MAX

```python
LOG_LINES_MAX = 200
```

Maximum number of log messages displayed before older entries are removed.

---

# Assistant Modes

The assistant supports multiple operating modes.

```python
MODES = ("AI", "PC", "GAME")
```

Available modes:

| Mode | Purpose                        |
| ---- | ------------------------------ |
| AI   | Natural language conversations |
| PC   | Desktop automation             |
| GAME | Gesture-controlled gameplay    |

---

## MODE_COLORS

Defines the display color for each mode.

```python
MODE_COLORS = {
    "AI": "#00E5FF",
    "PC": "#4DFF88",
    "GAME": "#FF8C42",
}
```

---

# Voice Recognition

## WAKE_WORD

```python
WAKE_WORD = "jarvis"
```

The word that activates the assistant.

Example:

```
Jarvis, open Firefox.
```

---

## VOSK_MODEL_PATH

Path to the local Vosk speech recognition model.

```python
VOSK_MODEL_PATH
```

This path should point to an installed Vosk model directory.

---

## SAMPLE_RATE

```python
SAMPLE_RATE = 16000
```

Recommended sample rate for speech recognition.

Changing this value is generally not recommended.

---

## CHANNELS

```python
CHANNELS = 1
```

Mono microphone input.

---

## INPUT_DEVICE

```python
INPUT_DEVICE = None
```

Allows manually selecting a microphone.

Leave as `None` to use the system default.

---

# AI Memory

## MEMORY_MAX_TURNS

```python
MEMORY_MAX_TURNS = 8
```

Controls how many conversation turns remain in memory.

Higher values improve conversational context but require more memory.

Recommended:

```
8–12
```

---

# Desktop Automation

## APP_WHITELIST

Defines which applications the assistant is allowed to launch.

Example:

```python
chrome

notepad

calculator
```

Applications not listed here cannot be opened through voice commands.

This prevents unintended execution of arbitrary programs.

---

# Voice Cancellation

## CANCEL_PHRASES

```python
[
"jarvis stop",
"jarvis cancel",
"stop",
"cancel"
]
```

Commands that immediately stop the current action.

---

## REQUIRE_WAKE_FOR_CANCEL

```python
True
```

If enabled, cancellation requires the wake word to avoid accidental interruptions.

Recommended value:

```
True
```

---

# Mouse & Keyboard Safety

These settings prevent dangerous or accidental automation.

---

## PYAUTOGUI_FAILSAFE

```python
True
```

Moving the mouse to the top-left corner immediately aborts automation.

This setting should always remain enabled.

---

## PYAUTOGUI_PAUSE

```python
0.08
```

Adds a short delay between automation actions.

Prevents commands from executing too quickly.

---

## INPUT_RATE_LIMIT_S

```python
0.35
```

Minimum time between automation commands.

Reduces accidental repeated actions.

---

## TYPE_MAX_CHARS

```python
120
```

Maximum number of characters the assistant may type automatically.

This prevents accidental pasting of very large text blocks.

---

# Allowed Keys

```python
ALLOWED_KEYS
```

Defines which keyboard keys may be pressed.

Examples include:

* Enter
* Escape
* Tab
* Backspace
* Space

Adding additional keys should be done carefully.

---

# Allowed Hotkeys

```python
ALLOWED_HOTKEYS
```

Safe keyboard shortcuts available to the assistant.

Examples:

* Copy
* Paste
* Select All
* Alt+Tab

---

# Risky Hotkeys

```python
RISKY_HOTKEYS
```

These shortcuts require additional confirmation before execution.

Example:

```
Alt + F4
```

---

## CONFIRM_WINDOW_S

```python
5.0
```

Number of seconds the user has to confirm risky actions.

---

# Game Mode

## GAME_MODE_DEFAULT

```python
False
```

Determines whether the assistant starts directly in Game Mode.

Recommended:

```
False
```

---

## GAME_KEYMAP

Maps spoken commands to keyboard keys.

Example:

| Command | Key   |
| ------- | ----- |
| left    | A     |
| right   | D     |
| jump    | Space |
| fire    | F     |
| reload  | R     |

Users can modify this mapping to support different games.

---

# Whisper Speech Recognition

## WHISPER_MODEL_SIZE

```python
small
```

Recommended values:

| Model  | Speed     | Accuracy  |
| ------ | --------- | --------- |
| tiny   | Very Fast | Low       |
| base   | Fast      | Medium    |
| small  | Good      | High      |
| medium | Slower    | Very High |
| large  | Slowest   | Best      |

For most users:

```
small
```

is recommended.

---

## WHISPER_DEVICE

```python
cuda
```

Possible values:

```
cpu
cuda
```

Use `cpu` if no NVIDIA GPU is available.

---

## WHISPER_COMPUTE_TYPE

```python
float16
```

Recommended:

* `float16` for GPU
* `int8` for CPU

---

## WHISPER_MAX_SECONDS

Maximum recording duration after the wake word.

```python
4.0
```

---

## WHISPER_MIN_SECONDS

Minimum recording length.

```python
3
```

---

## WHISPER_SILENCE_MS

```python
450
```

Recording automatically stops after this amount of silence.

---

## WHISPER_ENERGY_THRESH

```python
400
```

Microphone sensitivity threshold.

Lower values increase sensitivity.

Higher values reduce background noise.

---

# Demo Mode

## DEMO_ENABLED

```python
True
```

Enables automatic demonstration mode.

---

## DEMO_IDLE_SECONDS

```python
12
```

Idle time before demo mode starts.

---

## DEMO_MESSAGE_EVERY

```python
6
```

Interval between demo messages.

---

# Game Launcher

## AUTO_LAUNCH_GAME_ON_GAME_MODE

```python
True
```

Automatically launches the configured game when Game Mode is enabled.

---

## GAME_EXE_PATH

Absolute path to a game executable.

Leave empty when using Microsoft Store or Steam launch methods.

---

## GAME_WORKING_DIR

Working directory for the game executable.

---

## GAME_PROCESS_NAME

Used to detect whether the game is already running.

---

## GAME_APP_ID

Microsoft Store application identifier.

Example:

```
VectorUnit.BeachBuggyRacing_hvbhrz8672s2!App
```

---

# Recommended Configuration

For systems with **4 GB RAM**:

| Setting       | Recommended Value |
| ------------- | ----------------- |
| AI Model      | gemma3:1b         |
| Whisper Model | small             |
| Device        | CPU               |
| Memory Turns  | 8                 |
| Demo Mode     | Enabled           |
| Fail Safe     | Enabled           |

---

# Best Practices

* Keep the application whitelist as small as possible.
* Leave fail-safe mode enabled.
* Test new hotkeys before daily use.
* Avoid increasing memory limits on low-end hardware.
* Use CPU-friendly AI models on systems without dedicated GPUs.
* Regularly review configuration changes before deployment.

---

# Summary

The `config.py` file provides a single location for customizing the behavior of Jarvis AI Assistant. By separating configuration from implementation, the project becomes easier to maintain, safer to operate, and more accessible for contributors. Whether adjusting the user interface, changing the AI model, tuning speech recognition, or modifying game controls, nearly every aspect of the assistant can be configured without changing the core application logic.
