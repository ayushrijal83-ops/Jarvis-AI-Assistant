# 🤖 Jarvis AI Assistant

### An Offline AI Desktop Assistant Powered by Local Large Language Models

> Privacy-first • Offline-first • Modular • Open Source

---

# 📖 Table of Contents

- Overview
- Features
- Screenshots
- Demo
- Architecture
- Technology Stack
- Quick Start
- Installation
- AI Model Setup
- Speech Recognition Setup
- Continue in `README_Part2.md`

---

# 🚀 Overview

Jarvis AI Assistant is a modular offline desktop assistant powered by local AI. It combines local LLMs, speech recognition, computer vision, gesture recognition, desktop automation and game control into one application.

## ✨ Features

- Local LLM (Ollama)
- Offline speech recognition
- Gesture recognition
- Computer vision
- Desktop automation
- Game mode
- Emotion engine
- Conversation memory

# 📷 Screenshots

_Add screenshots here._

# 🎥 Demo

_Add GIF or YouTube demo here._

# 🏗 Architecture

```text
User
 │
 ├── Voice
 ├── Camera
 └── Keyboard
      │
 Command Router
      │
 ├── AI Brain
 ├── Vision
 ├── Desktop Controller
 └── Game Controller
```

# ⚙ Technology Stack

| Component | Technology |
|---|---|
| Language | Python |
| LLM | Ollama |
| Vision | OpenCV |
| Gestures | MediaPipe |
| Speech | Vosk / Faster-Whisper |
| Automation | PyAutoGUI |

# ⚡ Quick Start

```bash
git clone https://github.com/ayushrijal83-ops/Jarvis-AI-Assistant.git
cd Jarvis-AI-Assistant
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Linux/macOS

```bash
source venv/bin/activate
```

```bash
pip install -r requirements.txt
```

# 🧠 AI Model Setup

Install Ollama from https://ollama.com/download

```bash
ollama serve
ollama pull mistral
```

Alternative models:

- gemma3:1b
- phi3
- llama3

# 🎤 Speech Recognition Setup

Install:

```bash
pip install vosk
```

Download a Vosk model from the official Vosk models page and extract it to:

```text
models/
└── vosk-model-small-en-us-0.15/
```

> Large AI models are intentionally excluded from this repository because of GitHub size limits.
# ▶ Continue from Part 1

# ⚙ Configuration

Edit `config.py` to change the LLM model, speech model path, camera settings and automation preferences.

# 📁 Project Structure

```text
Jarvis-AI-Assistant/
├── assets/
├── docs/
├── models/
├── src/
├── main.py
├── config.py
├── requirements.txt
└── README.md
```

# ▶ Usage

```bash
python main.py
```

# 🔄 Workflow

User → Speech/Camera → Recognition → Command Router → AI Brain → Desktop Actions

# 💻 Recommended Hardware

Minimum:
- 8 GB RAM
- Intel i5 / Ryzen 5

Recommended:
- 16 GB RAM
- SSD
- Webcam
- Microphone

# 🔒 Why Local AI?

- No API costs
- Better privacy
- Offline capable
- Local inference

# 🛠 Troubleshooting

## Ollama not found
Restart your terminal.

## Missing model
Run `ollama pull mistral`.

## Speech model missing
Download and place it inside `models/`.

# 🗺 Roadmap

## v1.0
- Local LLM
- Voice Recognition
- Vision
- Gestures
- Desktop Automation

## v1.5
- Face Recognition
- Better UI
- Plugins

## v2.0
- Long-term Memory
- RAG
- AI Agents

# 📚 Documentation

Create additional docs:
- SETUP_MODELS.md
- ARCHITECTURE.md
- VOICE_SYSTEM.md
- GAME_MODE.md

# 🤝 Contributing

Fork the repository, create a branch, commit your changes, and open a Pull Request.

# 📄 License

MIT License.

# 🙏 Acknowledgements

Thanks to the communities behind Ollama, OpenCV, MediaPipe, Vosk, Faster-Whisper and Python.

---

⭐ If you find this project useful, consider giving it a star!
