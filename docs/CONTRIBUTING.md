# 🤝 Contributing to Jarvis AI Assistant

First off, **thank you for considering contributing to the Jarvis AI Assistant!** 🎉

Whether you're fixing a typo, improving documentation, reporting bugs, or implementing new features, your contributions help make this project better for everyone.

---

# Table of Contents

* Welcome
* Code of Conduct
* Ways to Contribute
* Getting Started
* Development Setup
* Branch Strategy
* Coding Standards
* Documentation Standards
* Commit Message Guidelines
* Pull Request Process
* Reporting Bugs
* Suggesting Features
* Testing Requirements
* Security Guidelines
* Community
* Recognition

---

# Welcome

Jarvis AI Assistant is an open-source, privacy-first AI desktop assistant that combines:

* 🤖 Local AI (Ollama)
* 🎤 Voice Recognition
* ✋ Gesture Control
* 🖥 Desktop Automation
* 🎮 Game Controller
* 👁 Computer Vision

Our goal is to build one of the best offline AI assistants available.

---

# Code of Conduct

Please be respectful and professional.

We expect contributors to:

* Be respectful
* Be patient
* Accept constructive criticism
* Help newcomers
* Use inclusive language
* Focus on improving the project

Harassment or abusive behavior will not be tolerated.

---

# Ways to Contribute

There are many ways to help.

### Documentation

* Improve explanations
* Fix grammar
* Add examples
* Update screenshots
* Expand tutorials

---

### Bug Fixes

* Fix crashes
* Improve stability
* Resolve compatibility issues
* Improve error handling

---

### New Features

Examples:

* New AI models
* Better gesture recognition
* Voice improvements
* New automation commands
* Game profiles
* Performance optimizations

---

### Testing

Help test:

* Windows
* Linux
* Different AI models
* Various webcams
* Different microphones

---

# Getting Started

## 1. Fork the Repository

Click the **Fork** button on GitHub.

---

## 2. Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/Jarvis-AI-Assistant.git
```

---

## 3. Navigate to the Project

```bash
cd Jarvis-AI-Assistant
```

---

## 4. Create a Virtual Environment

```bash
python -m venv venv
```

---

## 5. Activate the Environment

Windows

```bash
venv\Scripts\activate
```

Linux/macOS

```bash
source venv/bin/activate
```

---

## 6. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 7. Start Ollama

```bash
ollama serve
```

---

# Development Workflow

Recommended workflow:

```text
Fork Repository

↓

Clone Repository

↓

Create Feature Branch

↓

Write Code

↓

Run Tests

↓

Commit Changes

↓

Push Branch

↓

Open Pull Request

↓

Code Review

↓

Merge
```

---

# Branch Naming

Use descriptive branch names.

Examples:

```text
feature/voice-improvements

feature/new-gesture

feature/game-profile

bugfix/camera-crash

bugfix/audio-delay

docs/update-readme

refactor/command-router
```

---

# Coding Standards

Follow **PEP 8** for Python code.

General guidelines:

* Use meaningful variable names.
* Keep functions short.
* Add docstrings.
* Avoid duplicated code.
* Write modular code.
* Handle exceptions properly.

Example:

```python
def open_application(name: str) -> bool:
    """
    Open an approved desktop application.

    Args:
        name: Name of the application.

    Returns:
        True if successful, otherwise False.
    """
```

---

# Documentation Standards

When adding a new feature:

* Update the README if needed.
* Document new configuration options.
* Add examples.
* Update architecture diagrams if the design changes.
* Add a dedicated document for major modules.

Documentation is considered part of the feature.

---

# Commit Message Guidelines

Use clear, concise commit messages.

Format:

```text
type: short description
```

Examples:

```text
feat: add custom wake word support

fix: resolve microphone initialization issue

docs: improve installation guide

refactor: simplify gesture classifier

test: add unit tests for AI Brain

perf: reduce camera processing latency
```

Common commit types:

| Type     | Purpose                  |
| -------- | ------------------------ |
| feat     | New feature              |
| fix      | Bug fix                  |
| docs     | Documentation            |
| refactor | Code restructuring       |
| test     | Testing                  |
| perf     | Performance improvements |
| chore    | Maintenance tasks        |

---

# Pull Request Checklist

Before submitting a Pull Request, ensure that:

* Code builds successfully.
* Tests pass.
* Documentation has been updated.
* No unnecessary files are included.
* Code follows project standards.
* New features include appropriate comments.
* Configuration changes are documented.

---

# Reporting Bugs

When reporting a bug, include:

* Operating system
* Python version
* Jarvis version
* Hardware information
* Error message
* Steps to reproduce
* Screenshots (if applicable)
* Relevant log files

Detailed bug reports help resolve issues faster.

---

# Suggesting Features

Feature requests should include:

* Problem description
* Proposed solution
* Expected behavior
* Possible implementation ideas
* Benefits to users

Constructive suggestions are always welcome.

---

# Testing Requirements

Before opening a Pull Request:

* Run the application.
* Verify there are no syntax errors.
* Test new functionality.
* Ensure existing functionality still works.
* Check for regressions.

If possible, test on multiple operating systems.

---

# Security Guidelines

Security is a core principle of Jarvis AI Assistant.

Please do not introduce features that:

* Execute arbitrary commands without validation.
* Disable safety mechanisms.
* Bypass application whitelists.
* Expose sensitive user information.
* Require unnecessary cloud services.

If you discover a security issue, report it privately before creating a public issue.

---

# Community Communication

Be respectful in:

* GitHub Issues
* Pull Requests
* Discussions
* Code Reviews

Constructive feedback leads to better software.

---

# Recognition

Every contributor is appreciated.

Contributors may be recognized through:

* GitHub Contributors page
* Release notes
* Project documentation
* Community acknowledgements

Thank you for helping improve the project.

---

# Questions?

If you have questions:

* Read the documentation.
* Search existing Issues.
* Check the FAQ.
* Open a GitHub Discussion or Issue if needed.

We are happy to help new contributors get started.

---

# Thank You ❤️

Every contribution—whether it's fixing a typo, improving documentation, reporting a bug, or developing a major feature—helps make the Jarvis AI Assistant better.

Together, we can build a powerful, privacy-focused, offline AI assistant for everyone.
