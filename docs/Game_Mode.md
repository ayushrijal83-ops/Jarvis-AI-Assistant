# 🎮 Game Mode

## Introduction

**Game Mode** transforms the Jarvis AI Assistant into a real-time gaming controller. Instead of controlling the operating system through voice commands alone, users can interact with supported games using hand gestures, keyboard commands, or other input methods.

The module is designed to provide a responsive, low-latency experience while maintaining the safety and modularity principles used throughout the project.

---

# Objectives

Game Mode was designed with the following goals:

* Real-time game control
* Gesture-based interaction
* Low input latency
* Configurable control mappings
* Easy game integration
* Safe keyboard automation
* Modular architecture
* Future plugin support

---

# Responsibilities

The Game Mode module is responsible for:

* Activating gaming mode
* Receiving gesture events
* Translating gestures into game controls
* Sending keyboard inputs
* Managing game profiles
* Launching supported games
* Monitoring game state

---

# High-Level Architecture

```text
                  User
          ┌────────┴────────┐
          │                 │
          ▼                 ▼
   Gesture Control     Voice Commands
          │                 │
          └────────┬────────┘
                   ▼
            Game Controller
                   │
        ┌──────────┼──────────┐
        │          │          │
        ▼          ▼          ▼
 Keyboard Input Mouse Input Game Launcher
        │
        ▼
      Running Game
```

---

# System Components

## 1. Game Controller

The Game Controller is the core of Game Mode.

Responsibilities include:

* Receiving gesture events
* Mapping actions
* Sending keyboard input
* Managing game state
* Switching profiles

---

## 2. Input Mapper

The Input Mapper converts recognized gestures into keyboard or mouse actions.

Example:

| Gesture | Keyboard Key     |
| ------- | ---------------- |
| Left    | A                |
| Right   | D                |
| Up      | Space            |
| Down    | S                |
| Fist    | Left Mouse Click |
| Palm    | Pause            |

Mappings can be customized to match different games.

---

## 3. Game Launcher

The Game Launcher can automatically start a supported game when Game Mode is enabled.

Supported launch methods include:

* Executable path
* Steam shortcut
* Microsoft Store App ID

The launcher also checks whether the game is already running.

---

## 4. Profile Manager

Different games require different controls.

The Profile Manager stores game-specific mappings so users can switch between games without changing the source code.

Example:

```text
Beach Buggy Racing
↓

Left  → A
Right → D
Jump  → Space
Brake → S
```

---

# Game Mode Workflow

```text
User Enables Game Mode

↓

Load Game Profile

↓

Launch Game (Optional)

↓

Enable Gesture Recognition

↓

Receive Gesture

↓

Convert to Keyboard Input

↓

Game Receives Input
```

---

# Gesture-to-Key Translation

The Game Controller receives gesture events from the Gesture Control System.

Example flow:

```text
Hand Gesture

↓

Gesture Recognized

↓

Game Controller

↓

Keyboard Event

↓

Game
```

This separation keeps gesture recognition independent from game-specific logic.

---

# Voice Commands

Game Mode also supports voice commands.

Examples:

```text
Jarvis, start game mode.

Jarvis, stop game mode.

Jarvis, pause game.

Jarvis, resume game.

Jarvis, launch Beach Buggy Racing.
```

Voice commands are routed through the Command Router before reaching the Game Controller.

---

# Supported Input Types

The architecture supports multiple control methods.

Current support:

* Hand gestures
* Keyboard emulation
* Voice commands

Planned support:

* Eye tracking
* Blink detection
* Head movement
* Gamepad integration
* Mobile controller

---

# Keyboard Emulation

Keyboard events are generated using safe desktop automation.

Supported actions include:

* Key press
* Key release
* Key hold
* Key combinations

All generated inputs pass through the same safety checks used by the PC Control System.

---

# Performance Optimization

To minimize latency during gameplay, the module uses:

* Event-driven processing
* Efficient gesture mapping
* Lightweight keyboard automation
* Independent processing threads
* Reusable game profiles

These optimizations help maintain a smooth gaming experience.

---

# Safety Mechanisms

Game Mode includes several protections to prevent unintended actions.

Features include:

* Game Mode toggle
* Emergency stop
* Rate limiting
* Allowed key validation
* Automatic cleanup when exiting

These mechanisms ensure that keyboard automation stops immediately when Game Mode is disabled.

---

# Error Handling

The Game Mode module handles common issues gracefully.

Examples include:

* Game not installed
* Invalid executable path
* Missing game profile
* Unsupported gesture
* Keyboard automation failure
* Camera unavailable

When an error occurs, users receive descriptive feedback while the rest of the assistant continues running.

---

# Configuration

Most Game Mode settings are configurable through `config.py`.

Common settings include:

| Setting              | Description                  |
| -------------------- | ---------------------------- |
| Default Game Mode    | Enable on startup            |
| Auto Launch Game     | Start game automatically     |
| Game Executable Path | Path to the game             |
| Working Directory    | Game launch directory        |
| Process Name         | Running process detection    |
| Key Mapping          | Gesture-to-key configuration |

---

# Example Control Profile

| Gesture | Action     | Keyboard   |
| ------- | ---------- | ---------- |
| Left    | Turn Left  | A          |
| Right   | Turn Right | D          |
| Up      | Jump       | Space      |
| Down    | Brake      | S          |
| Fist    | Fire       | Left Mouse |
| Palm    | Pause      | Esc        |

Users can create additional profiles for different games without modifying the Game Controller itself.

---

# Future Enhancements

Planned improvements include:

* Plugin-based game profiles
* Automatic game detection
* Multi-game switching
* Eye-controlled gameplay
* Gesture recording
* Custom gesture editor
* Cloud profile synchronization (optional)
* Multiplayer input sharing
* Macro recording
* AI-assisted control suggestions

The modular architecture allows these features to be added without major changes to the existing system.

---

# Typical Game Session

```text
User

↓

"Jarvis, start game mode"

↓

Game Controller

↓

Load Profile

↓

Launch Game

↓

Enable Gesture Recognition

↓

Recognize Gestures

↓

Generate Keyboard Events

↓

Game Responds
```

---

# Design Principles

Game Mode follows the same engineering principles as the rest of the project:

* Modularity
* Low latency
* Safety first
* Offline operation
* Extensibility
* Maintainability
* Separation of concerns

These principles make the module reliable while allowing future enhancements.

---

# Advantages

Game Mode provides several benefits:

* Hands-free gameplay
* Customizable controls
* Easy game integration
* Low resource usage
* Offline operation
* Modular design
* Safe automation
* Expandable architecture

---

# Summary

Game Mode extends the Jarvis AI Assistant beyond desktop automation by enabling real-time interaction with games through gestures, voice commands, and keyboard emulation. Its modular design separates gesture recognition, input mapping, and game management into independent components, making it easy to support new games and interaction methods while maintaining low latency, strong safety mechanisms, and an excellent user experience.
