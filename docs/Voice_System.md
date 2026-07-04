# 🎤 Voice System

## Introduction

The **Voice System** is one of the primary interaction methods of the Jarvis AI Assistant. It enables users to communicate naturally using spoken language instead of relying on a keyboard or mouse.

Unlike many commercial assistants, the Voice System is designed to work **offline**, ensuring user privacy while providing fast and reliable speech recognition.

---

# Objectives

The Voice System was designed with the following goals:

* Offline speech recognition
* Fast command processing
* Wake-word activation
* Low latency
* High recognition accuracy
* Modular architecture
* Easy model replacement
* Noise tolerance

---

# Responsibilities

The Voice System is responsible for:

* Listening to microphone input
* Detecting the wake word
* Recording user speech
* Converting speech into text
* Forwarding recognized commands to the Command Router
* Handling speech recognition errors
* Managing microphone resources

---

# High-Level Architecture

```text
                 User Speaks
                      │
                      ▼
                 Microphone
                      │
                      ▼
              Audio Capture
                      │
                      ▼
             Wake Word Detector
                      │
          Wake Word Detected?
              │            │
             No           Yes
              │            │
      Continue Listening   ▼
                      Record Speech
                            │
                            ▼
                    Faster Whisper
                            │
                            ▼
                    Recognized Text
                            │
                            ▼
                    Command Router
                            │
                            ▼
                     AI / PC / Game
```

---

# Components

The Voice System consists of several independent components.

## 1. Audio Capture

Responsible for:

* Reading microphone data
* Maintaining audio buffers
* Sampling audio
* Detecting silence

---

## 2. Wake Word Detection

The assistant continuously listens for a predefined wake word.

Example:

```text
Jarvis...
```

Only after detecting the wake word does the assistant begin recording the user's command.

Advantages:

* Prevents accidental activation
* Reduces unnecessary AI processing
* Conserves CPU resources

---

## 3. Voice Recording

Once activated, the assistant records speech until one of the following occurs:

* User stops speaking
* Maximum recording time is reached
* Silence timeout expires
* Cancel phrase is detected

---

## 4. Speech Recognition

Recorded audio is passed to the **Faster Whisper** speech recognition engine.

The model converts audio into text that can be processed by the assistant.

Example:

```text
Audio

↓

Faster Whisper

↓

"Open Firefox"
```

---

## 5. Command Forwarding

After speech is converted into text, the recognized command is sent to the Command Router.

The router decides whether the request should be handled by:

* AI Brain
* PC Controller
* Game Controller

---

# Audio Pipeline

```text
Microphone

↓

Audio Buffer

↓

Wake Word Detection

↓

Speech Recording

↓

Silence Detection

↓

Faster Whisper

↓

Text Command

↓

Command Router
```

---

# Wake Word System

The wake word acts as a trigger for the assistant.

Example:

```text
Jarvis, open Firefox.

Jarvis, search YouTube.

Jarvis, what is Python?

Jarvis, start game mode.
```

Advantages:

* Hands-free interaction
* Reduced false positives
* Improved user experience

---

# Supported Commands

Examples of commands include:

### AI

```text
Jarvis, explain machine learning.
```

---

### PC Control

```text
Jarvis, open calculator.
```

---

### Browser

```text
Jarvis, search GitHub.
```

---

### Game Mode

```text
Jarvis, start game mode.
```

---

# Noise Handling

Background noise is one of the biggest challenges in speech recognition.

The Voice System reduces errors by using:

* Energy threshold detection
* Silence detection
* Limited recording duration
* Wake-word activation
* Configurable microphone sensitivity

These mechanisms improve recognition accuracy in everyday environments.

---

# Microphone Configuration

The microphone can be configured through `config.py`.

Typical settings include:

| Setting          | Description                  |
| ---------------- | ---------------------------- |
| Sample Rate      | Audio sampling frequency     |
| Channels         | Mono or stereo               |
| Input Device     | Selected microphone          |
| Energy Threshold | Minimum volume level         |
| Silence Timeout  | Stop recording after silence |

---

# Faster Whisper

The project uses **Faster Whisper** for offline speech recognition.

Benefits include:

* High accuracy
* Fast inference
* Offline operation
* Low memory usage
* CPU and GPU support

---

# Model Selection

Several Whisper models are available.

| Model  | Speed | Accuracy |
| ------ | ----- | -------- |
| Tiny   | ⭐⭐⭐⭐⭐ | ⭐⭐       |
| Base   | ⭐⭐⭐⭐  | ⭐⭐⭐      |
| Small  | ⭐⭐⭐   | ⭐⭐⭐⭐     |
| Medium | ⭐⭐    | ⭐⭐⭐⭐⭐    |
| Large  | ⭐     | ⭐⭐⭐⭐⭐    |

For low-end systems, the **Small** model provides a good balance between speed and accuracy.

---

# Error Handling

The Voice System gracefully handles common problems.

Examples include:

* Microphone unavailable
* Audio device disconnected
* Recognition timeout
* Empty speech
* Background noise
* Invalid audio format

Whenever possible, meaningful feedback is provided instead of terminating the application.

---

# Performance Optimization

Several techniques help improve responsiveness:

* Continuous audio buffering
* Limited recording duration
* Efficient silence detection
* Lightweight speech model
* Streaming audio processing

These optimizations reduce latency while keeping CPU usage manageable.

---

# Privacy

The Voice System follows an offline-first philosophy.

Benefits include:

* No cloud speech APIs
* No internet required
* No voice recordings uploaded
* Local speech processing
* Complete user control

This ensures voice data remains on the user's computer.

---

# Future Improvements

Planned enhancements include:

* Multi-language recognition
* Speaker identification
* Voice authentication
* Custom wake words
* Real-time streaming transcription
* Voice activity detection improvements
* Noise suppression
* Automatic language detection

---

# Voice Processing Flow

```text
User Speaks
      │
      ▼
Microphone
      │
      ▼
Wake Word Detection
      │
      ▼
Speech Recording
      │
      ▼
Faster Whisper
      │
      ▼
Recognized Text
      │
      ▼
Command Router
      │
      ▼
AI Brain / PC Controller / Game Controller
      │
      ▼
Assistant Response
```

---

# Design Principles

The Voice System follows these engineering principles:

* Modularity
* Reliability
* Offline-first operation
* Privacy by design
* Low latency
* Extensibility
* Fault tolerance

These principles make it easy to replace or upgrade the speech recognition engine without affecting other modules.

---

# Summary

The Voice System provides a natural and efficient way to interact with the Jarvis AI Assistant. By combining wake-word detection, offline speech recognition with Faster Whisper, configurable audio processing, and seamless integration with the Command Router, it enables responsive, private, and hands-free control of the assistant while remaining flexible enough to support future enhancements.
