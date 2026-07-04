# 📚 Internal API Documentation

## Introduction

The Jarvis AI Assistant is built using a **modular architecture**, where each subsystem exposes a well-defined interface to the rest of the application. Instead of allowing every module to communicate directly with every other module, communication occurs through clearly defined APIs and the Command Router.

This document explains the internal APIs, module responsibilities, data flow, events, and extension points for developers.

---

# API Architecture

```text
                     User
                       │
                       ▼
                Voice / Gesture
                       │
                       ▼
               Command Router API
                       │
      ┌────────────────┼────────────────┐
      │                │                │
      ▼                ▼                ▼
   AI API        PC Control API    Game API
      │                │                │
      └────────────────┼────────────────┘
                       ▼
                  System Response
```

---

# Module Communication

Modules never manipulate each other directly.

Instead, every request follows this sequence:

```text
Input

↓

Router

↓

Target Module

↓

Response

↓

UI
```

This architecture reduces coupling and makes debugging significantly easier.

---

# Core Modules

| Module            | Responsibility          |
| ----------------- | ----------------------- |
| main.py           | Application entry point |
| ai_brain.py       | AI communication        |
| voice.py          | Speech recognition      |
| control.py        | Desktop automation      |
| gesture.py        | Gesture recognition     |
| game_mode.py      | Game controller         |
| emotion_engine.py | Context awareness       |
| config.py         | Project configuration   |

---

# Main Application API

## Responsibilities

* Initialize modules
* Load configuration
* Start worker threads
* Create GUI
* Handle shutdown

Typical lifecycle:

```text
Load Config

↓

Initialize Modules

↓

Start Threads

↓

Wait For Events

↓

Shutdown
```

---

# AI Brain API

## Public Responsibilities

* Receive prompts
* Build conversation context
* Communicate with Ollama
* Return streaming responses

Example interface:

```python
generate_response(prompt)

clear_history()

set_model(model_name)
```

---

# Voice System API

## Public Responsibilities

* Listen continuously
* Detect wake word
* Convert speech to text
* Forward commands

Example interface:

```python
start_listener()

stop_listener()

transcribe(audio)
```

---

# PC Controller API

## Public Responsibilities

* Open applications
* Open websites
* Type text
* Press keys
* Execute safe automation

Example interface:

```python
open_application(name)

search_web(query)

type_text(text)

press_key(key)
```

---

# Gesture Control API

## Public Responsibilities

* Start webcam
* Detect hand landmarks
* Classify gestures
* Emit gesture events

Example interface:

```python
start_camera()

stop_camera()

detect_gesture(frame)
```

---

# Game Controller API

## Public Responsibilities

* Enable Game Mode
* Disable Game Mode
* Load game profiles
* Translate gestures

Example interface:

```python
enable()

disable()

load_profile(name)
```

---

# Emotion Engine API

## Public Responsibilities

* Analyze interaction state
* Update context
* Share recommendations

Example interface:

```python
update_context(data)

get_state()

reset()
```

---

# Configuration API

The configuration module exposes project-wide settings.

Example:

```python
config.WAKE_WORD

config.WHISPER_MODEL

config.APP_TITLE
```

Every module imports configuration values from a single location.

---

# Event System

Most modules communicate through events.

Examples:

```text
VOICE_COMMAND

↓

ROUTER

↓

AI_REQUEST
```

---

```text
GESTURE_DETECTED

↓

GAME_CONTROLLER

↓

KEYBOARD_EVENT
```

---

```text
PC_COMMAND

↓

PC_CONTROLLER

↓

DESKTOP_ACTION
```

---

# Data Objects

Several common data types are shared throughout the application.

## Voice Command

```text
{
    text,
    timestamp,
    confidence
}
```

---

## Gesture Event

```text
{
    gesture,
    confidence,
    timestamp
}
```

---

## AI Response

```text
{
    response,
    tokens,
    duration
}
```

---

## Desktop Action

```text
{
    action,
    target,
    status
}
```

---

# Error Handling

Each module returns structured error information rather than terminating the application.

Example:

```text
{
    success: false,
    error: "Camera unavailable"
}
```

This simplifies debugging and improves reliability.

---

# Thread Model

Several components operate concurrently.

```text
Main Thread

├── GUI

├── Voice Thread

├── Camera Thread

├── AI Thread

├── Game Thread
```

Separating workloads improves responsiveness and prevents long-running tasks from blocking the user interface.

---

# Logging API

Every module writes consistent log entries.

Typical log information:

* Timestamp
* Module
* Action
* Status
* Error (if present)

Example:

```text
[12:45:18]

Module:
Voice

Action:
Wake Word Detected

Status:
Success
```

---

# Extension Points

The architecture allows developers to extend Jarvis without modifying existing modules.

Examples:

* Add a new AI model
* Create a new gesture
* Add a new desktop command
* Support additional games
* Integrate new sensors
* Add plugins
* Add new automation workflows

---

# Dependency Overview

```text
main.py

│

├── config.py

├── ai_brain.py

├── voice.py

├── control.py

├── gesture.py

├── emotion_engine.py

└── game_mode.py
```

Each module depends on the configuration layer while remaining largely independent from one another.

---

# API Design Principles

The internal APIs follow several principles:

* Single responsibility
* Loose coupling
* Clear interfaces
* Error resilience
* Extensibility
* Reusability
* Maintainability

These principles simplify future development and testing.

---

# Versioning

As the project evolves, API compatibility should follow semantic versioning:

| Version | Meaning                                     |
| ------- | ------------------------------------------- |
| Major   | Breaking API changes                        |
| Minor   | New features without breaking compatibility |
| Patch   | Bug fixes and internal improvements         |

Maintaining version consistency helps contributors understand compatibility expectations.

---

# Future API Enhancements

Planned improvements include:

* Plugin API
* WebSocket API
* REST API
* Remote client support
* Mobile companion integration
* Custom automation plugins
* Third-party AI provider adapters
* Event subscription system

These additions will allow Jarvis to integrate with a wider range of applications and services.

---

# Summary

The internal API provides a structured communication layer between the modules that make up the Jarvis AI Assistant. By using well-defined interfaces, shared data structures, and an event-driven design, the project remains modular, maintainable, and easy to extend. This architecture allows developers to add new capabilities while minimizing the impact on existing components.
