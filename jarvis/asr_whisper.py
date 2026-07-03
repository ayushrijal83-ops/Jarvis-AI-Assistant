# asr_whisper.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from faster_whisper import WhisperModel


@dataclass
class WhisperConfig:
    model_size: str = "small"      # tiny / base / small / medium / large-v3
    device: str = "cpu"            # "cpu" first; later: "cuda"
    compute_type: str = "int8"     # cpu: int8 is fast + good


class WhisperASR:
    """
    Offline Whisper ASR using faster-whisper (CTranslate2).
    Designed for short command clips after wake word.
    """

    def __init__(self, cfg: Optional[WhisperConfig] = None):
        self.cfg = cfg or WhisperConfig()
        self._model: Optional[WhisperModel] = None

    def _ensure(self):
        if self._model is None:
            self._model = WhisperModel(
                self.cfg.model_size,
                device=self.cfg.device,
                compute_type=self.cfg.compute_type,
            )

    def transcribe_wav(self, wav_path: str) -> str:
        """
        Returns best text transcription for a short wav clip.
        """
        self._ensure()
        segments, info = self._model.transcribe(
            wav_path,
            vad_filter=True,
        )
        text = " ".join(seg.text.strip() for seg in segments).strip()
        return text
