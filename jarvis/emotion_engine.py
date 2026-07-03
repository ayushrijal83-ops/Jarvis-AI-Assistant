# emotion_engine.py

class EmotionEngine:
    """
    Lightweight context interpreter.
    NO ML, NO threads, NO side effects.
    """

    def __init__(self):
        self._state = "UNKNOWN"

    def update(self, vision_state: str):
        if vision_state:
            self._state = vision_state.upper()

    def style_hint(self) -> str:
        """
        Returns a style hint: 'normal', 'short'
        """
        if self._state in ("DISTRACTED", "LOOKING DOWN", "FACE LOST"):
            return "short"

        if self._state == "DROWSY":
            return "short"

        return "normal"
