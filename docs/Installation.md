# 📦 Installation Guide

## Introduction

Welcome to the **Jarvis AI Assistant** installation guide.

This document provides a complete walkthrough for setting up the assistant from scratch on a new computer.

By the end of this guide, you will have:

* Python installed
* Ollama installed
* A local Large Language Model downloaded
* All required Python packages installed
* The project running successfully

---

# System Requirements

## Minimum Requirements

| Component  | Requirement                  |
| ---------- | ---------------------------- |
| CPU        | Intel i3 (10th Gen or newer) |
| RAM        | 4 GB                         |
| Storage    | 5 GB free                    |
| Python     | 3.11+                        |
| Webcam     | Optional (Gesture & Vision)  |
| Microphone | Required (Voice Commands)    |
| Internet   | Only for initial setup       |

---

## Recommended Requirements

| Component | Requirement        |
| --------- | ------------------ |
| CPU       | Intel i5 / Ryzen 5 |
| RAM       | 8 GB or more       |
| GPU       | NVIDIA (Optional)  |
| Storage   | SSD                |

---

# 1. Clone the Repository

```bash
git clone https://github.com/ayushrijal83-ops/Jarvis-AI-Assistant.git
```

Move into the project folder:

```bash
cd Jarvis-AI-Assistant
```

---

# 2. Install Python

Download the latest version from:

https://www.python.org/downloads/

Verify installation:

```bash
python --version
```

Expected output:

```text
Python 3.11.x
```

---

# 3. Create a Virtual Environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

# 4. Upgrade pip

```bash
python -m pip install --upgrade pip
```

---

# 5. Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

# 6. Install Ollama

Download Ollama:

https://ollama.com/download

Verify installation:

```bash
ollama --version
```

---

# 7. Download a Local AI Model

Recommended for low-end systems:

```bash
ollama pull gemma3:1b
```

Other supported models:

```bash
ollama pull mistral
```

```bash
ollama pull qwen2.5:1.5b
```

```bash
ollama pull tinyllama
```

---

# 8. Start the Ollama Server

```bash
ollama serve
```

Keep this terminal running while using Jarvis.

---

# 9. Configure the Project

Open:

```text
config.py
```

Configure:

* Wake word
* AI model
* Voice settings
* Camera settings
* Game settings
* Keyboard shortcuts

---

# 10. Install Optional Dependencies

For Gesture Recognition:

```bash
pip install mediapipe opencv-python
```

For Voice Recognition:

```bash
pip install faster-whisper
```

For Desktop Automation:

```bash
pip install pyautogui
```

---

# 11. Verify Your Camera

Run:

```bash
python
```

```python
import cv2

camera = cv2.VideoCapture(0)

print(camera.isOpened())
```

Expected output:

```text
True
```

---

# 12. Verify Your Microphone

```bash
python
```

```python
import sounddevice as sd

print(sd.query_devices())
```

Ensure your microphone appears in the device list.

---

# 13. Run the Assistant

```bash
python main.py
```

The application should launch successfully.

---

# Updating the Project

Pull the latest changes:

```bash
git pull
```

Update Python packages:

```bash
pip install -r requirements.txt --upgrade
```

---

# Troubleshooting

## Python not found

Ensure Python is added to your system PATH.

---

## Ollama not detected

Verify installation:

```bash
ollama --version
```

Restart your computer if necessary.

---

## Model not found

Download the required model:

```bash
ollama pull gemma3:1b
```

---

## Camera not working

* Check camera permissions.
* Close other applications using the webcam.
* Ensure the correct camera index is selected.

---

## Microphone not working

* Verify operating system permissions.
* Select the correct input device.
* Test with another recording application.

---

## AI is not responding

Make sure the Ollama server is running:

```bash
ollama serve
```

---

# Supported Operating Systems

| Operating System | Status          |
| ---------------- | --------------- |
| Windows 10       | ✅ Supported     |
| Windows 11       | ✅ Supported     |
| Ubuntu           | ✅ Supported     |
| Debian           | ✅ Supported     |
| Fedora           | ✅ Supported     |
| Arch Linux       | ✅ Supported     |
| macOS            | ⚠️ Experimental |

---

# Next Step

Once the installation is complete, continue with the **Architecture Guide** to understand how the system is designed and how the different modules communicate with one another.
