# 🏗️ System Architecture

## Introduction

The **Jarvis AI Assistant** follows a **modular, event-driven architecture**. Every major capability—AI, voice recognition, gesture recognition, computer vision, PC automation, and game control—is implemented as an independent module.

This design keeps the project:

* Easy to maintain
* Easy to extend
* Easier to debug
* Scalable for future features

Instead of creating one large script, the assistant is divided into multiple components that communicate through events and shared interfaces.

---

# High-Level Architecture

```text
                               USER
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
        ▼                        ▼                        ▼
  Voice Input              Camera Input             Keyboard/Mouse
        │                        │
        ▼                        ▼
 Speech Recognition      Gesture & Vision
        │                        │
        └───────────────┬────────┘
                        ▼
                 Command Router
                        │
      ┌─────────────────┼─────────────────┐
      │                 │                 │
      ▼                 ▼                 ▼
   AI Brain      PC Controller     Game Controller
      │                 │                 │
      └─────────────────┼─────────────────┘
                        ▼
                 Desktop Interaction
```

---

# System Components

The project is divided into several independent modules.

## 1. Main Application

**File**

```text
main.py
```

Responsibilities:

* Starts all modules
* Initializes the event queue
* Starts the voice system
* Starts the gesture manager
* Starts the vision system
* Creates the graphical interface
* Performs graceful shutdown

The `main.py` file acts as the application's entry point and coordinates the lifecycle of all major components.

---

## 2. AI Brain

**File**

```text
ai_brain.py
```

Responsibilities:

* Connect to Ollama
* Send prompts to the selected language model
* Stream responses
* Maintain short-term conversation memory
* Handle AI errors safely

The AI Brain is responsible for natural language understanding and response generation while keeping conversations local.

---

## 3. Voice Recognition

Responsibilities:

* Listen to the microphone
* Detect the wake word
* Record voice commands
* Convert speech into text
* Send commands to the router

The voice module enables natural interaction with the assistant without relying on cloud services.

---

## 4. Gesture Recognition

Responsibilities:

* Capture webcam frames
* Detect hand landmarks
* Classify gestures
* Send gesture events to the game controller

Supported gesture categories include:

* Left
* Right
* Palm
* Hand
* Fist

---

## 5. Vision System

Responsibilities:

* Access camera frames
* Analyze user presence
* Monitor attention
* Share visual information with other modules

The vision module can later be extended with face recognition, object detection, or scene understanding.

---

## 6. Emotion Engine

Responsibilities:

* Interpret user attention state
* Adjust interaction style
* Provide contextual hints to other modules

Rather than performing full emotion recognition, this lightweight component adapts the assistant's behavior based on contextual signals.

---

## 7. PC Controller

Responsibilities:

* Launch applications
* Search the web
* Control keyboard input
* Control mouse input
* Execute safe desktop actions

Security mechanisms such as whitelists and rate limiting help prevent accidental automation.

---

## 8. Game Controller

Responsibilities:

* Translate gestures into game controls
* Manage game profiles
* Send keyboard events
* Launch supported games

Game-specific logic is separated from the rest of the assistant, making it easy to add new profiles in the future.

---

# Data Flow

The following sequence shows how a typical voice command is processed.

```text
User speaks

↓

Microphone

↓

Speech Recognition

↓

Text Command

↓

Command Router

↓

AI Brain / PC Controller / Game Controller

↓

Response

↓

User
```

---

# Event-Driven Design

The assistant uses an **event queue** to allow modules to communicate without tightly depending on one another.

Advantages include:

* Loose coupling
* Easier testing
* Better responsiveness
* Simpler debugging
* Improved scalability

---

# Threading Model

Several modules operate concurrently to improve responsiveness.

Examples include:

* Voice listener
* Gesture recognition
* Vision processing
* User interface
* Game controller

Running these components independently ensures that heavy tasks such as AI inference do not block the graphical interface or input processing.

---

# AI Request Flow

```text
User Prompt

↓

Command Router

↓

AI Brain

↓

Ollama

↓

Local Language Model

↓

Streaming Response

↓

Assistant Output
```

This approach enables local inference while preserving user privacy.

---

# Voice Pipeline

```text
Microphone

↓

Wake Word Detection

↓

Speech Recording

↓

Whisper ASR

↓

Text

↓

Command Router
```

---

# Gesture Pipeline

```text
Camera

↓

MediaPipe

↓

Hand Landmarks

↓

Gesture Classification

↓

Game Controller

↓

Keyboard Events
```

---

# PC Automation Pipeline

```text
User Command

↓

Command Router

↓

PC Controller

↓

Safe Validation

↓

Desktop Action
```

---

# Memory Flow

```text
User Message

↓

Conversation History

↓

AI Brain

↓

Assistant Response

↓

Memory Update
```

Only a limited amount of conversation history is stored in memory to keep the assistant responsive.

---

# Error Handling

Every module is designed to fail gracefully.

Examples include:

* Camera unavailable
* Microphone unavailable
* AI model offline
* Invalid application request
* Gesture recognition failure

Instead of crashing, the assistant reports the issue and continues running whenever possible.

---

# Security Design

Safety is a core design goal.

Current protections include:

* Application whitelist
* Restricted keyboard actions
* Rate-limited automation
* PyAutoGUI fail-safe support
* Configurable settings
* Offline-first AI

---

# Design Principles

The project follows several software engineering principles:

* Modularity
* Separation of concerns
* Offline-first design
* Extensibility
* Maintainability
* Reusability
* User safety

These principles make the assistant easier to extend as new features are added.

---

# Future Architecture

The current architecture provides a strong foundation for future enhancements such as:

* Plugin system
* Multi-agent architecture
* Long-term memory
* Face recognition
* Speaker identification
* Retrieval-Augmented Generation (RAG)
* Web automation
* Smart scheduling
* Mobile companion application

The modular design ensures these capabilities can be integrated without major changes to the existing codebase.

---

# Summary

Jarvis AI Assistant is designed as a collection of independent modules working together through an event-driven architecture. This approach enables offline AI interaction, desktop automation, gesture recognition, computer vision, and future extensibility while maintaining a clean and maintainable codebase.
