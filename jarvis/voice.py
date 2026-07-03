# voice.py
from __future__ import annotations

from emotion_engine import EmotionEngine


import json
import queue
import threading
import time
import wave
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import numpy as np
import sounddevice as sd
import pyttsx3
from vosk import Model, KaldiRecognizer

from utils import UiEvent
from shared_state import set_game_mode, is_game_mode

from config import (
    WAKE_WORD,
    VOSK_MODEL_PATH,
    SAMPLE_RATE,
    CHANNELS,
    INPUT_DEVICE,
    CANCEL_PHRASES,
    REQUIRE_WAKE_FOR_CANCEL,
    WHISPER_MODEL_SIZE,
    WHISPER_DEVICE,
    WHISPER_COMPUTE_TYPE,
    WHISPER_MAX_SECONDS,
)

# Optional config values (safe defaults if missing)
try:
    from config import WHISPER_MIN_SECONDS, WHISPER_SILENCE_MS, WHISPER_ENERGY_THRESH
except Exception:
    WHISPER_MIN_SECONDS = 0.9
    WHISPER_SILENCE_MS = 450
    WHISPER_ENERGY_THRESH = 400


@dataclass
class VoiceConfig:
    wake_word: str = WAKE_WORD
    sample_rate: int = SAMPLE_RATE
    channels: int = CHANNELS
    input_device: Optional[int] = INPUT_DEVICE


class VoiceManager:
    """
    FULL UPGRADED VoiceManager (Offline-first, stable):
    - Vosk: wake word + cancel during TTS
    - Whisper: accurate command transcription (after wake)
    - Smart recording: stops on silence
    - Echo protection: no full ASR while speaking + cooldown + mic drain
    - Human-aware TTS: pauses on DISTRACTED/LOOKING DOWN, resumes on ATTENTIVE/LOOKING CENTER
    - Deterministic PC actions BEFORE AI
    - AI (Ollama AIBrain) + fallback rules
    - Game Mode synced via shared_state (UI button + voice always match)
    """

    def __init__(self, event_q: "queue.Queue[UiEvent]", cfg: VoiceConfig | None = None):
        self.event_q = event_q
        self.cfg = cfg or VoiceConfig()

        self._emotion = EmotionEngine()

        # stop/threads
        self._stop = threading.Event()
        self._listen_thread: Optional[threading.Thread] = None
        self._speak_thread: Optional[threading.Thread] = None
        self._capture_thread: Optional[threading.Thread] = None

        # audio queue (from RawInputStream callback)
        self._audio_q: "queue.Queue[bytes]" = queue.Queue(maxsize=160)

        # TTS queue + interrupt
        self._tts_q: "queue.Queue[str]" = queue.Queue()
        self._tts_interrupt = threading.Event()

        # speaking flags + cooldown
        self._is_speaking = threading.Event()
        self._asr_resume_time = 0.0
        self._post_tts_cooldown_s = 0.35

        # models
        self._vosk_model: Optional[Model] = None
        self._cancel_recognizer: Optional[KaldiRecognizer] = None
        self._whisper = None

        # AI brain
        self._brain = None

        # capture gate
        self._capturing = threading.Event()

        # confirmation state
        self._pending_confirm: Optional[str] = None
        self._pending_confirm_ts: float = 0.0

        # ---- Human-aware TTS state ----
        self._attention_ok = True
        self._paused_by_attention = False
        self._resume_text = ""
        self._resume_lock = threading.Lock()

        # temp wav path
        self._tmp_dir = Path(__file__).resolve().parent / "tmp"
        self._tmp_dir.mkdir(exist_ok=True)

    # ---------------- UI helpers ----------------
    def _ui_state(self, state: str, log: str | None = None):
        self.event_q.put(UiEvent(type="state", payload={"state": state, "log": log}))

    def _ui_log(self, text: str):
        self.event_q.put(UiEvent(type="log", payload={"text": text}))

    def _ui_error(self, text: str):
        self.event_q.put(UiEvent(type="state", payload={"state": "ERROR", "log": text}))

    # ---------------- lifecycle ----------------
    def start(self):
        if not VOSK_MODEL_PATH.exists():
            self._ui_error(f"[error] Vosk model not found at: {VOSK_MODEL_PATH}")
            return

        try:
            self._vosk_model = Model(str(VOSK_MODEL_PATH))
        except Exception as e:
            self._ui_error(f"[error] Failed to load Vosk model: {e}")
            return

        self._stop.clear()

        self._speak_thread = threading.Thread(target=self._speaker_loop, daemon=True)
        self._listen_thread = threading.Thread(target=self._listener_loop, daemon=True)
        self._speak_thread.start()
        self._listen_thread.start()

        self._ui_log("[system] Voice started (Vosk wake + Whisper command). Say 'Jarvis'.")

    def stop(self):
        self._stop.set()
        self._tts_interrupt.set()
        with self._resume_lock:
            self._resume_text = ""
        self._ui_log("[system] Voice stopping...")

    # ---------------- Vision callback (Phase 6.4) ----------------
    def on_vision_state(self, state: str):
        self._emotion.update(state)

        """
        Called from UI thread when Vision emits states.
        Pause/resume speaking based on attention.
        """
        s = (state or "").upper()

        # Pause triggers
        if s in ("DISTRACTED", "LOOKING DOWN"):
            self._attention_ok = False
            self._paused_by_attention = True
            # Interrupt speech (speaker loop will store remaining)
            self._tts_interrupt.set()
            return

        # Resume triggers
        if s in ("ATTENTIVE", "LOOKING CENTER"):
            self._attention_ok = True
            # resume any pending remaining text, race-free
            with self._resume_lock:
                remaining = self._resume_text
                self._resume_text = ""

            if remaining and (not self._is_speaking.is_set()):
                self._paused_by_attention = False
                self._tts_q.put(remaining)

    # ---------------- helpers ----------------
    def _drain_audio_queue(self, max_items: int = 800):
        n = 0
        while n < max_items:
            try:
                self._audio_q.get_nowait()
                n += 1
            except queue.Empty:
                break

    def _lazy_whisper(self):
        if self._whisper is None:
            from asr_whisper import WhisperASR, WhisperConfig
            self._whisper = WhisperASR(
                WhisperConfig(
                    model_size=WHISPER_MODEL_SIZE,
                    device=WHISPER_DEVICE,
                    compute_type=WHISPER_COMPUTE_TYPE,
                )
            )

    # ---------------- confirmation helpers ----------------
    def _start_confirmation(self, action_name: str):
        try:
            from config import CONFIRM_WINDOW_S
        except Exception:
            # fallback safety
            self._pending_confirm = None
            return

        self._pending_confirm = action_name
        self._pending_confirm_ts = time.time()
        self._ui_log(f"[system] Confirm pending: {action_name}")
        self.speak(f"Confirm {action_name}. Say yes to proceed.")

    def _consume_confirmation(self, t: str) -> Optional[str]:
        if not self._pending_confirm:
            return None

        try:
            from config import CONFIRM_WINDOW_S
        except Exception:
            CONFIRM_WINDOW_S = 5.0

        if (time.time() - self._pending_confirm_ts) > CONFIRM_WINDOW_S:
            self._pending_confirm = None
            return "Confirmation timed out."

        if t in {"yes", "confirm", "do it"}:
            action = self._pending_confirm
            self._pending_confirm = None
            return f"Confirmed: {action}"

        if t in {"no", "cancel", "stop"}:
            self._pending_confirm = None
            return "Cancelled."

        return None

    # ---------------- TTS ----------------
    def speak(self, text: str):
        """
        Queue speech. This interrupts current speech.
        """
        if not text:
            return
        self._tts_interrupt.set()
        self._tts_q.put(text)

    def _speaker_loop(self):
        engine = pyttsx3.init()
        engine.setProperty("rate", 185)

        while not self._stop.is_set():
            try:
                text = self._tts_q.get(timeout=0.1)
            except queue.Empty:
                continue

            if not text:
                continue

            # Start speaking
            self._tts_interrupt.clear()
            self._is_speaking.set()
            self._ui_state("SPEAKING", "[system] TTS speaking...")

            words = text.split()
            pos = 0
            spoke_all = True
            chunk: list[str] = []

            while pos < len(words):
                # global stop
                if self._stop.is_set():
                    spoke_all = False
                    break

                # manual interrupt OR pause signal OR attention gate
                if self._tts_interrupt.is_set() or (not self._attention_ok):
                    spoke_all = False
                    if not self._attention_ok:
                        self._paused_by_attention = True
                    try:
                        engine.stop()
                    except Exception:
                        pass
                    break

                chunk.append(words[pos])
                pos += 1

                if len(chunk) >= 10:
                    engine.say(" ".join(chunk))
                    engine.runAndWait()
                    chunk.clear()

            # speak remaining chunk only if not interrupted
            if spoke_all and chunk:
                engine.say(" ".join(chunk))
                engine.runAndWait()

            # if interrupted, save remaining for resume (unless it was a HARD stop)
            if not spoke_all and pos < len(words):
                remaining = " ".join(words[pos:]).strip()
                if remaining:
                    with self._resume_lock:
                        # Only store resume text if we paused due to attention
                        if self._paused_by_attention:
                            self._resume_text = remaining
                        else:
                            # manual stop: discard resume
                            self._resume_text = ""

            # end speaking
            self._is_speaking.clear()
            self._asr_resume_time = time.time() + self._post_tts_cooldown_s
            self._drain_audio_queue()
            self._ui_state("IDLE", None)

        try:
            engine.stop()
        except Exception:
            pass

    # ---------------- ASR - audio callback ----------------
    def _audio_callback(self, indata, frames, time_info, status):
        if status:
            self._ui_log(f"[warn] Audio status: {status}")
        try:
            self._audio_q.put_nowait(bytes(indata))
        except queue.Full:
            # drop frames to keep realtime
            pass

    # ---------------- Smart recording for Whisper ----------------
    def _record_command_wav_smart(self, max_seconds: float) -> str:
        """
        Record a short command clip and stop early on silence.
        Uses a separate InputStream so it doesn't depend on RawInputStream buffer timing.
        """
        max_seconds = float(max_seconds)
        max_frames = int(self.cfg.sample_rate * max_seconds)

        min_frames = int(self.cfg.sample_rate * float(WHISPER_MIN_SECONDS))
        silence_needed = int(self.cfg.sample_rate * (float(WHISPER_SILENCE_MS) / 1000.0))
        chunk_frames = int(self.cfg.sample_rate * 0.12)  # ~120ms

        audio_chunks = []
        total_frames = 0
        silence_run = 0

        stream = sd.InputStream(
            samplerate=self.cfg.sample_rate,
            channels=self.cfg.channels,
            dtype="int16",
            device=self.cfg.input_device,
        )

        with stream:
            while total_frames < max_frames and not self._stop.is_set():
                data, _ = stream.read(chunk_frames)
                audio_chunks.append(data.copy())
                total_frames += len(data)

                mono = data[:, 0] if data.ndim == 2 else data
                energy = int(np.mean(np.abs(mono)))

                if energy < int(WHISPER_ENERGY_THRESH):
                    silence_run += len(data)
                else:
                    silence_run = 0

                if total_frames >= min_frames and silence_run >= silence_needed:
                    break

        audio = np.concatenate(audio_chunks, axis=0) if audio_chunks else np.zeros((0, self.cfg.channels), dtype=np.int16)

        wav_path = str(self._tmp_dir / "cmd.wav")
        with wave.open(wav_path, "wb") as wf:
            wf.setnchannels(self.cfg.channels)
            wf.setsampwidth(2)  # int16
            wf.setframerate(self.cfg.sample_rate)
            wf.writeframes(audio.tobytes())

        return wav_path

    # ---------------- Wake + Cancel loop (Vosk) ----------------
    def _listener_loop(self):
        assert self._vosk_model is not None

        wake_rec = KaldiRecognizer(self._vosk_model, self.cfg.sample_rate)
        wake_rec.SetWords(False)

        # Cancel recognizer used ONLY while speaking/cooldown
        try:
            cancel_grammar = json.dumps([p.lower() for p in CANCEL_PHRASES])
            self._cancel_recognizer = KaldiRecognizer(self._vosk_model, self.cfg.sample_rate, cancel_grammar)
            self._cancel_recognizer.SetWords(False)
        except Exception as e:
            self._cancel_recognizer = None
            self._ui_log(f"[warn] Cancel recognizer disabled: {e}")

        try:
            stream = sd.RawInputStream(
                samplerate=self.cfg.sample_rate,
                blocksize=8000,
                dtype="int16",
                channels=self.cfg.channels,
                callback=self._audio_callback,
                device=self.cfg.input_device,
            )
        except Exception as e:
            self._ui_error(f"[error] Microphone/stream init failed: {e}")
            return

        self._ui_log("[system] Mic ready. Say 'Jarvis'.")

        with stream:
            while not self._stop.is_set():

                # During speaking/cooldown: only listen for cancel keywords
                if self._is_speaking.is_set() or time.time() < self._asr_resume_time:
                    try:
                        data = self._audio_q.get(timeout=0.1)
                    except queue.Empty:
                        continue

                    if self._cancel_recognizer and self._cancel_recognizer.AcceptWaveform(data):
                        try:
                            res = json.loads(self._cancel_recognizer.Result())
                        except Exception:
                            continue

                        heard = (res.get("text") or "").strip().lower()
                        if heard:
                            if REQUIRE_WAKE_FOR_CANCEL:
                                if "jarvis" in heard and ("stop" in heard or "cancel" in heard):
                                    self._hard_stop_speaking()
                            else:
                                if "stop" in heard or "cancel" in heard:
                                    self._hard_stop_speaking()
                    continue

                # If we are already capturing a command, ignore wake listening
                if self._capturing.is_set():
                    time.sleep(0.03)
                    continue

                try:
                    data = self._audio_q.get(timeout=0.1)
                except queue.Empty:
                    continue

                if wake_rec.AcceptWaveform(data):
                    try:
                        res = json.loads(wake_rec.Result())
                    except Exception:
                        continue

                    text = (res.get("text") or "").strip().lower()
                    if not text:
                        continue

                    self._ui_log(f"[vosk] {text}")

                    wake = self.cfg.wake_word.lower()
                    if wake in text.split():
                        if not self._capturing.is_set():
                            self._capturing.set()
                            self._capture_thread = threading.Thread(
                                target=self._capture_and_process_command,
                                daemon=True,
                            )
                            self._capture_thread.start()

        self._ui_log("[system] Listener loop exited.")

    # ---------------- Hard stop (discard resume) ----------------
    def _hard_stop_speaking(self):
        """
        True stop: interrupt TTS + discard any resume text.
        """
        self._tts_interrupt.set()
        self._paused_by_attention = False
        with self._resume_lock:
            self._resume_text = ""
        self._ui_log("[system] Cancel detected: stopped speaking.")

    # ---------------- Capture + route command ----------------
    def _capture_and_process_command(self):
        """
        Triggered after wake word.
        Records command via smart capture and transcribes with Whisper.
        """
        try:
            # Wait out TTS cooldown
            while self._is_speaking.is_set() or time.time() < self._asr_resume_time:
                if self._stop.is_set():
                    return
                time.sleep(0.02)

            self._ui_state("LISTENING", "[system] Listening (Whisper)...")

            # Record short command
            wav_path = self._record_command_wav_smart(WHISPER_MAX_SECONDS)

            # Transcribe
            cmd_text = ""
            try:
                self._lazy_whisper()
                cmd_text = (self._whisper.transcribe_wav(wav_path) or "").strip().lower()
            except Exception as e:
                self._ui_error(f"[error] Whisper failed, fallback enabled: {e}")

            if not cmd_text:
                self._ui_log("[whisper] (empty)")
                self.speak("I didn't catch that. Please try again.")
                return

            self._ui_log(f"[whisper] {cmd_text}")

            self._ui_state("THINKING", "[system] Processing command...")
            response = self._route(cmd_text)

            if not response:
                response = "I didn't get a response. Please try again."

            self._ui_log(f"[jarvis] {response}")
            self.speak(response)

        finally:
            self._capturing.clear()
            self._ui_state("IDLE", None)

    # ---------------- Router ----------------
    def _route(self, text: str) -> str:
        t = (text or "").strip().lower()
        if not t:
            return ""

        # Always interrupt ongoing speech on new recognition (misheard safeguard)
        self._tts_interrupt.set()

        # confirmations first
        c = self._consume_confirmation(t)
        if c:
            if c.startswith("Confirmed:"):
                action_name = c.replace("Confirmed:", "", 1).strip().lower()
                try:
                    from control import PCController
                    pc = PCController()
                    ok, msg = pc.hotkey(action_name)
                    return msg
                except Exception as e:
                    self._ui_error(f"[error] Confirmed action failed: {e}")
                    return "Failed to execute confirmed action."
            return c

        # hard stop words
        if any(k in t for k in ("stop", "cancel", "shut up", "silence")):
            self._hard_stop_speaking()
            return "Stopped."

        # game mode toggles (synced with UI button)
        if t in ("game mode on", "enable game mode", "race mode on"):
            set_game_mode(True)
            self._ui_state("GAME", "[system] Game Mode enabled")

            try:
                from game_launcher import launch_game_if_needed
                ok, msg = launch_game_if_needed(self.event_q)
                if not ok:
                    self._ui_log(f"[warn] {msg}")
                return f"Game mode enabled. {msg}"
            except Exception as e:  
                self._ui_log(f"[warn] Game auto-launch failed: {e}")
                return "Game mode enabled."


        if t in ("game mode off", "disable game mode", "race mode off"):
            set_game_mode(False)
            self._ui_state("IDLE", "[system] Game Mode disabled")
            return "Game mode disabled."

        # If game mode active, keep voice safe (gestures control gameplay)
        if is_game_mode():
            return "Game mode is active. Use gestures, or say game mode off."

        # deterministic PC controls before AI
        try:
            from control import PCController
            pc = PCController()

            if t.startswith("open "):
                app = t.replace("open", "", 1).strip()
                ok, msg = pc.open_app(app)
                return msg

            if "what apps can you open" in t:
                apps = ", ".join(pc.list_apps())
                return f"I can open: {apps}"

            if t.startswith("search "):
                q = t.replace("search", "", 1).strip()
                ok, msg = pc.search_web(q)
                return msg

            if t.startswith("google "):
                q = t.replace("google", "", 1).strip()
                ok, msg = pc.search_web(q)
                return msg

            if t in ("click", "mouse click"):
                ok, msg = pc.click()
                return msg

            if t in ("double click", "doubleclick"):
                ok, msg = pc.double_click()
                return msg

            if t.startswith("scroll "):
                direction = t.replace("scroll", "", 1).strip()
                ok, msg = pc.scroll(direction)
                return msg

            if t.startswith("type "):
                txt = text.strip()[5:]  # preserve original casing
                ok, msg = pc.type_text(txt)
                return msg

            if t.startswith("press "):
                key = t.replace("press", "", 1).strip()
                ok, msg = pc.press_key(key)
                return msg

            # hotkeys with confirmation
            try:
                from config import ALLOWED_HOTKEYS, RISKY_HOTKEYS
                if t in ALLOWED_HOTKEYS:
                    if t in RISKY_HOTKEYS:
                        self._start_confirmation(t)
                        return "Waiting for confirmation."
                    ok, msg = pc.hotkey(t)
                    return msg
            except Exception:
                pass

        except Exception as e:
            self._ui_error(f"[error] PC/Input control failed: {e}")
            # continue to AI

        # AI init once
        try:
            if self._brain is None:
                from ai_brain import AIBrain
                self._brain = AIBrain()
        except Exception as e:
            self._ui_error(f"[error] AI init failed, fallback enabled: {e}")
            return self._rule_response(text)

        # memory controls
        if any(k in t for k in ("clear memory", "reset memory", "forget everything", "wipe memory")):
            try:
                self._brain.reset_memory()
            except Exception:
                pass
            self._ui_log("[system] Memory cleared.")
            return "Memory cleared."

        if any(k in t for k in ("what did i say", "recall", "show memory")):
            try:
                hist = getattr(self._brain, "_history", None)
                if not hist:
                    return "Memory is empty."
                recent_user = [m["content"] for m in list(hist)[-12:] if m.get("role") == "user"]
                if not recent_user:
                    return "Memory is empty."
                return "Recent things you said: " + " | ".join(recent_user[-4:])
            except Exception:
                return "I couldn't read memory safely."

        # filler
        if len(t.split()) <= 1 and t in {"yes", "yeah", "ok", "okay", "hmm", "yo"}:
            return "Ready."

        # AI call
        self._ui_state("THINKING", "[system] Sending to Ollama...")
        try:
            out = self._brain.generate(text)
            if out and out.strip():
                return out.strip()
            return "I didn't get a response. Please try again."
        except Exception as e:
            self._ui_error(f"[error] Ollama failed, fallback enabled: {e}")
            return self._rule_response(text)

    # ---------------- fallback ----------------
    def _rule_response(self, text: str) -> str:
        t = (text or "").lower()
        if "your name" in t:
            return "I am Jarvis. Offline fallback is active."
        if "help" in t:
            return "Say Jarvis, then speak your command."
        return f"You said: {text}"


def print_mic_devices():
    """Run manually if sounddevice picks the wrong microphone."""
    print(sd.query_devices())
