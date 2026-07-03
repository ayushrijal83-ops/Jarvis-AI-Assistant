# ai_brain.py
from __future__ import annotations

import time
from typing import Generator, List, Dict

try:
    import ollama
except Exception as e:
    ollama = None


class AIBrain:
    """
    Ollama AI Brain with STREAMING output (terminal-like speed)

    Features:
    - Streaming tokens (fast perceived response)
    - Short-term RAM memory (conversation context)
    - Safe fallback (never crashes app)
    - Designed for voice-first systems
    """

    def __init__(self, model: str = "mistral"):
        self.model = model
        self._history: List[Dict[str, str]] = []
        self.max_history = 10  # keep memory light & fast

    # --------------------------------------------------
    # STREAMING GENERATION (KEY FEATURE)
    # --------------------------------------------------
    def generate_stream(self, prompt: str) -> Generator[str, None, None]:
        """
        Stream response chunks from Ollama.
        Yields text parts as soon as they arrive.
        """
        if not ollama:
            yield "[AI offline]"
            return

        messages = self._history + [{"role": "user", "content": prompt}]
        full_response = ""

        try:
            stream = ollama.chat(
                model=self.model,
                messages=messages,
                stream=True
            )

            for chunk in stream:
                part = chunk.get("message", {}).get("content", "")
                if part:
                    full_response += part
                    yield part  # 🔥 FAST: token streaming

        except Exception as e:
            yield "I'm having trouble thinking right now."
            return

        # Save memory AFTER full response
        self._remember(prompt, full_response)

    # --------------------------------------------------
    # BLOCKING GENERATION (fallback / optional)
    # --------------------------------------------------
    def generate(self, prompt: str) -> str:
        """
        Blocking generation (safe fallback).
        """
        if not ollama:
            return "AI is offline."

        try:
            res = ollama.chat(
                model=self.model,
                messages=self._history + [{"role": "user", "content": prompt}],
            )
            text = res["message"]["content"]
            self._remember(prompt, text)
            return text
        except Exception:
            return "I couldn't generate a response."

    # --------------------------------------------------
    # MEMORY MANAGEMENT
    # --------------------------------------------------
    def _remember(self, user_text: str, assistant_text: str):
        self._history.append({"role": "user", "content": user_text})
        self._history.append({"role": "assistant", "content": assistant_text})

        # Trim memory (keep system fast)
        if len(self._history) > self.max_history * 2:
            self._history = self._history[-self.max_history * 2 :]

    def reset_memory(self):
        self._history.clear()

    # --------------------------------------------------
    # DEBUG / INTROSPECTION (OPTIONAL)
    # --------------------------------------------------
    def memory_snapshot(self) -> List[str]:
        return [m["content"] for m in self._history if m["role"] == "user"]
