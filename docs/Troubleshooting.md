# 🛠️ Troubleshooting Guide

## Introduction

This guide helps users diagnose and resolve the most common issues encountered while installing, configuring, and using the **Jarvis AI Assistant**.

Each section explains the symptoms, possible causes, and recommended solutions.

---

# Before You Start

Before troubleshooting, verify the following:

* Python 3.11 or later is installed.
* All required Python packages are installed.
* Ollama is installed and running.
* The selected AI model has been downloaded.
* Your webcam and microphone are connected.
* You are using the latest version of the project.

---

# Installation Problems

## Problem

```text
ModuleNotFoundError
```

### Possible Causes

* Missing dependency
* Virtual environment not activated
* Incorrect Python interpreter

### Solution

Activate the virtual environment.

```bash
source venv/bin/activate
```

or on Windows

```bash
venv\Scripts\activate
```

Install dependencies again.

```bash
pip install -r requirements.txt
```

---

## Problem

```text
pip command not found
```

### Solution

Check that Python and pip are installed.

```bash
python --version

pip --version
```

If pip is missing:

```bash
python -m ensurepip --upgrade
```

---

# Ollama Problems

## Problem

```text
Connection refused
```

### Cause

The Ollama server is not running.

### Solution

Start Ollama.

```bash
ollama serve
```

---

## Problem

```text
Model not found
```

### Cause

The required language model has not been downloaded.

### Solution

Download the model.

Example:

```bash
ollama pull gemma3:1b
```

Verify available models.

```bash
ollama list
```

---

## Problem

Slow AI responses

### Possible Causes

* Large model
* Low RAM
* CPU-only inference
* Other applications consuming resources

### Solutions

* Use a smaller model.
* Close unnecessary applications.
* Reduce conversation history.
* Upgrade system memory if possible.

---

# Voice Recognition Problems

## Problem

The assistant does not hear my voice.

### Possible Causes

* Wrong microphone selected
* Microphone muted
* Permission denied

### Solutions

* Check operating system audio settings.
* Verify the correct microphone is selected.
* Test the microphone using another application.

---

## Problem

Wake word is never detected.

### Possible Causes

* Incorrect wake word
* Background noise
* Low microphone sensitivity

### Solutions

* Speak clearly.
* Reduce environmental noise.
* Adjust microphone sensitivity in `config.py`.

---

## Problem

Speech recognition is inaccurate.

### Solutions

* Speak more clearly.
* Reduce background noise.
* Improve microphone quality.
* Use the recommended Whisper model.
* Position yourself closer to the microphone.

---

# Camera Problems

## Problem

```text
Cannot open camera
```

### Possible Causes

* Camera already in use
* Incorrect camera index
* Permission denied

### Solutions

* Close other camera applications.
* Verify the configured camera index.
* Restart the application.

---

## Problem

Black camera preview

### Solutions

* Check the webcam connection.
* Test the camera with another application.
* Reconnect the device.
* Restart the computer if necessary.

---

# Gesture Recognition Problems

## Problem

Gestures are not detected.

### Possible Causes

* Poor lighting
* Hand outside camera view
* Camera resolution too low

### Solutions

* Improve room lighting.
* Keep your hand fully visible.
* Use a higher camera resolution.
* Clean the camera lens.

---

## Problem

Incorrect gesture detected.

### Solutions

* Hold gestures steadily.
* Avoid overlapping hands.
* Keep fingers clearly separated.
* Update gesture mappings if required.

---

# PC Control Problems

## Problem

Applications do not open.

### Possible Causes

* Incorrect executable path
* Application not installed
* Whitelist restriction

### Solutions

* Verify the application is installed.
* Check the configured application path.
* Confirm the application is included in the whitelist.

---

## Problem

Keyboard automation does not work.

### Solutions

* Ensure Game Mode or PC Control is enabled.
* Check keyboard permissions.
* Restart the application.
* Test keyboard automation independently.

---

# Game Mode Problems

## Problem

Game does not respond.

### Possible Causes

* Incorrect key mappings
* Wrong game profile
* Game window not focused

### Solutions

* Load the correct profile.
* Verify keyboard mappings.
* Bring the game window into focus.

---

## Problem

High input latency

### Solutions

* Close unnecessary applications.
* Reduce camera resolution.
* Use a lighter Whisper model.
* Reduce AI model size if system resources are limited.

---

# Performance Issues

## High CPU Usage

Possible reasons:

* Camera processing
* Large AI model
* Multiple background applications

Solutions:

* Lower camera resolution.
* Reduce frame rate.
* Use a smaller AI model.
* Close unused software.

---

## High Memory Usage

Solutions:

* Use a smaller language model.
* Limit conversation history.
* Restart the application periodically.
* Close unused browser tabs and applications.

---

# Configuration Issues

## Problem

Changes to `config.py` have no effect.

### Solutions

* Save the file.
* Restart Jarvis.
* Check for syntax errors.
* Verify the correct configuration file is being loaded.

---

# Dependency Problems

## OpenCV Import Error

Reinstall OpenCV.

```bash
pip install --upgrade opencv-python
```

---

## MediaPipe Import Error

Reinstall MediaPipe.

```bash
pip install --upgrade mediapipe
```

---

## Faster Whisper Import Error

Reinstall Faster Whisper.

```bash
pip install --upgrade faster-whisper
```

---

# Logging

When troubleshooting, check the log files stored in the `logs/` directory.

Useful information includes:

* Startup errors
* Module initialization
* Voice events
* Gesture events
* AI requests
* Exception traces

Logs often provide the quickest way to identify the source of a problem.

---

# Debug Mode

For development, enable verbose logging in the configuration file.

Benefits include:

* Detailed error messages
* Performance metrics
* Module initialization status
* API communication logs
* Event tracing

Disable verbose logging in production to reduce unnecessary output.

---

# Reporting Issues

If the problem cannot be resolved, include the following information when opening a GitHub issue:

* Operating system
* Python version
* Jarvis version
* Hardware specifications
* Error message
* Steps to reproduce
* Relevant log files
* Screenshots (if applicable)

Providing detailed information helps maintainers reproduce and resolve issues more efficiently.

---

# Frequently Asked Questions

### Does Jarvis require an internet connection?

No. Core features such as AI conversations, speech recognition, gesture control, and desktop automation are designed to work offline after the required models are installed.

---

### Why is the first AI response slow?

The language model may take a few moments to load into memory on the first request. Subsequent responses are usually much faster.

---

### Can I use a different AI model?

Yes. Update the model name in `config.py` and ensure it has been downloaded through Ollama.

---

### Can I disable the webcam?

Yes. Camera-dependent features such as gesture recognition can be disabled without affecting the rest of the assistant.

---

### Why is my laptop fan running loudly?

Real-time AI inference, speech recognition, and computer vision are computationally intensive. Using smaller AI models or lowering the camera frame rate can reduce CPU usage.

---

# Getting Help

If you are still unable to resolve the issue:

1. Search existing GitHub Issues.
2. Review the project documentation.
3. Check the log files.
4. Open a new issue with detailed diagnostic information.

Constructive bug reports help improve the project for everyone.

---

# Summary

This troubleshooting guide covers the most common installation, configuration, performance, and runtime issues that users may encounter while using the Jarvis AI Assistant. By following the recommended diagnostic steps and solutions, most problems can be resolved quickly. For unresolved issues, detailed logs and reproducible reports will help contributors identify and fix bugs more effectively.
