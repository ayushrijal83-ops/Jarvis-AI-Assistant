<div align="center">

# 🤖 Jarvis AI Assistant

### An Offline AI Desktop Assistant Powered by Local Large Language Models

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-black?style=for-the-badge)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer_Vision-5C3EE8?style=for-the-badge&logo=opencv)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Gesture_Recognition-FF6F00?style=for-the-badge)
![Whisper](https://img.shields.io/badge/Faster--Whisper-Speech_Recognition-success?style=for-the-badge)
![MIT License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

</p>

**A modular AI assistant that combines Local LLMs, Voice Recognition, Computer Vision, Gesture Control, Desktop Automation, and Game Control into one offline application.**

---

⭐ **If you like this project, consider giving it a star!**

</div>

---

# 📖 Table of Contents

- Overview
- Features
- Screenshots
- Demo
- Architecture
- Technology Stack
- Installation
- Usage
- Folder Structure
- Project Workflow
- Roadmap
- Documentation
- Contributing
- License

---

# 🚀 Overview

Jarvis AI Assistant is an **offline-first desktop AI assistant** designed to perform intelligent computer interactions without relying on cloud services.

Instead of sending your conversations to online AI providers, Jarvis runs entirely on your own computer using **Ollama** and local language models.

The assistant combines multiple AI technologies into one unified system, including:

- Local Large Language Models
- Offline Speech Recognition
- Computer Vision
- Gesture Recognition
- Desktop Automation
- Keyboard & Mouse Control
- Game Control
- Modular Architecture

The project is designed for learning, research, experimentation, and future expansion.

---

# ✨ Features

## 🧠 Artificial Intelligence

- Local LLM using Ollama
- Streaming responses
- Conversation memory
- Context-aware conversations
- Offline inference

---

## 🎤 Voice Recognition

- Faster Whisper
- Offline speech recognition
- Wake-word support
- Low latency

---

## 🖥 Desktop Automation

- Open applications
- Search the web
- Mouse control
- Keyboard automation
- Safe application whitelist
- Rate limiting

---

## ✋ Gesture Recognition

- Hand tracking
- Gesture classification
- Camera interaction
- Real-time recognition

---

## 👁 Computer Vision

- Webcam integration
- User monitoring
- Attention tracking
- Frame processing

---

## 🎮 Game Mode

- Gesture-controlled gameplay
- Custom game profiles
- Automatic launcher
- Keyboard mapping

---

## 😊 Emotion Engine

- Context-aware response style
- Lightweight emotion handling
- Adaptive assistant behaviour

---

# 📷 Screenshots

> Screenshots will be added soon.

```
assets/screenshots/main_ui.png

assets/screenshots/voice_system.png

assets/screenshots/gesture_control.png

assets/screenshots/game_mode.png

assets/screenshots/vision.png
```

---

# 🎥 Demo

A demonstration video will be added after Version 1.0 is released.

---

# 🏗 System Architecture

```text
                    USER
                      │
      ┌───────────────┼────────────────┐
      │               │                │
      ▼               ▼                ▼
 Voice Input     Camera Input      Keyboard
      │               │
      ▼               ▼
Speech Engine    Vision Engine
      │               │
      └───────┬───────┘
              ▼
       Command Router
              │
 ┌────────────┼──────────────┐
 │            │              │
 ▼            ▼              ▼
AI Brain  PC Controller  Game Controller
 │            │              │
 └────────────┼──────────────┘
              ▼
      Desktop Interaction
```

---

# ⚙ Technology Stack

| Category | Technology |
|------------|------------|
| Programming Language | Python |
| Local AI | Ollama |
| Language Models | Mistral / Gemma / Llama |
| Speech Recognition | Faster Whisper |
| Computer Vision | OpenCV |
| Gesture Recognition | MediaPipe |
| Desktop Automation | PyAutoGUI |
| Audio Processing | SoundDevice |
| GUI | Tkinter |
| Threading | Python Threading |

---

# 📂 Project Structure

```
Jarvis-AI-Assistant/

│
├── assets/
│
├── docs/
│
├── models/
│
├── src/
│
├── main.py
├── ai_brain.py
├── control.py
├── gesture.py
├── gesture_control.py
├── emotion_engine.py
├── game_mode.py
├── config.py
│
├── requirements.txt
├── LICENSE
└── README.md
```

---

# ⚡ Installation

Clone the repository

```bash
git clone https://github.com/ayushrijal83-ops/Jarvis-AI-Assistant.git
```

Move into the project

```bash
cd Jarvis-AI-Assistant
```

Create a virtual environment

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Linux

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Install Ollama

```bash
https://ollama.com
```

Download a model

```bash
ollama pull mistral
```

or

```bash
ollama pull gemma3:1b
```

---

# ▶ Usage

Run the assistant

```bash
python main.py
```

---

# 🔄 Project Workflow

```
User

↓

Voice / Camera

↓

Recognition

↓

Command Router

↓

AI Brain

↓

Desktop Controller

↓

Action
```

---

# 📚 Documentation

Detailed documentation can be found in the **docs/** directory.

- Installation Guide
- Architecture
- AI Brain
- Voice System
- Gesture Control
- Vision System
- PC Control
- Game Mode
- API Documentation

---

# 🚀 Roadmap

## Version 1.0

- [x] Local LLM
- [x] Voice Recognition
- [x] Gesture Recognition
- [x] Desktop Automation
- [x] Game Mode
- [x] Emotion Engine

## Version 1.5

- [ ] Face Recognition
- [ ] Speaker Recognition
- [ ] Better UI
- [ ] Plugin System

## Version 2.0

- [ ] Long-Term Memory
- [ ] RAG
- [ ] Web Automation
- [ ] Smart Scheduling
- [ ] AI Agents

---

# 🤝 Contributing

Contributions are welcome.

If you have ideas, bug fixes, or new features, feel free to fork the repository and submit a Pull Request.

---

# 📄 License

This project is licensed under the MIT License.

---

# 🙏 Acknowledgements

This project uses several excellent open-source projects:

- Ollama
- Faster Whisper
- OpenCV
- MediaPipe
- PyAutoGUI
- Python

A big thanks to the open-source community for making local AI development accessible.

---

<div align="center">

## ⭐ Don't forget to Star the Repository ⭐

Made with ❤️ using Python and Open Source Technologies.

</div>
