import json
import requests
from utils import UiEvent

OLLAMA_URL = "http://localhost:11434/api/generate"

class OllamaClient:
    def __init__(self, event_q, model: str):
        self.event_q = event_q
        self.model = model

    def warmup(self):
        # Keeps model loaded so judge doesn't hit cold-start delay
        try:
            requests.post(
                OLLAMA_URL,
                json={"model": self.model, "prompt": "hi", "stream": False, "options": {"num_predict": 1}},
                timeout=5,
            )
        except Exception:
            pass

    def generate_stream(self, prompt: str, max_tokens: int = 160):
        """
        Streams tokens to UI using UiEvent(type="stream", payload={"text": token}).
        """
        self.event_q.put(UiEvent("state", {"state": "THINKING"}))
        self.event_q.put(UiEvent("log", {"text": "[jarvis] ", "tag": "jarvis"}))

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": True,
            "options": {
                "num_predict": max_tokens,
                "temperature": 0.6,
            },
        }

        try:
            with requests.post(OLLAMA_URL, json=payload, stream=True, timeout=60) as r:
                r.raise_for_status()
                for line in r.iter_lines(decode_unicode=True):
                    if not line:
                        continue
                    data = json.loads(line)
                    if "response" in data and data["response"]:
                        self.event_q.put(UiEvent("stream", {"text": data["response"], "tag": "jarvis"}))
                    if data.get("done"):
                        break
        except Exception as e:
            self.event_q.put(UiEvent("state", {"state": "ERROR"}))
            self.event_q.put(UiEvent("log", {"text": f"[error] Ollama stream failed: {e}"}))
            return

        self.event_q.put(UiEvent("stream", {"text": "\n"}))
        self.event_q.put(UiEvent("state", {"state": "IDLE"}))
