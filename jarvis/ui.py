# ui.py
from __future__ import annotations

import tkinter as tk
from queue import Queue, Empty
import math
import time
import random

from PIL import Image, ImageTk

from shared_state import set_game_mode, is_game_mode

from config import (
    APP_TITLE, BG, ACCENT, ACCENT_DIM, TEXT, ERROR,
    WIN_W, WIN_H, FPS_MS,
    CORE_RADIUS, RING_GAP, RING_COUNT, LOG_LINES_MAX
)
from utils import UiEvent, sin01

# Demo mode config (safe defaults)
try:
    from config import DEMO_ENABLED, DEMO_IDLE_SECONDS, DEMO_MESSAGE_EVERY
except Exception:
    DEMO_ENABLED = True
    DEMO_IDLE_SECONDS = 12
    DEMO_MESSAGE_EVERY = 6

# HUD palette
HUD_ORANGE = "#FF9A2E"
HUD_ORANGE_DIM = "#7A3E12"
HUD_CYAN = "#00F5FF"
HUD_GREEN = "#06D6A0"
HUD_YELLOW = "#FFD166"
HUD_RED = "#EF476F"


class JarvisUI:
    """
    Tkinter UI must run on the main thread.

    event_q: Queue[UiEvent]
    on_state_callback: optional callback for state events (e.g., voice.on_vision_state)
    frame_provider: optional callable returning latest frame (BGR numpy array) or (frame, ts)
    """

    def __init__(self, event_q: Queue, on_state_callback=None, frame_provider=None):
        self.event_q = event_q
        self.on_state_callback = on_state_callback
        self.frame_provider = frame_provider

        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.configure(bg=BG)
        self.root.overrideredirect(True)
        self._center_window(WIN_W, WIN_H)

        # Dragging for borderless window
        self._drag_offset = (0, 0)
        self.root.bind("<ButtonPress-1>", self._start_drag)
        self.root.bind("<B1-Motion>", self._do_drag)

        # Keybinds
        self.root.bind("<Escape>", lambda e: self.root.destroy())

        # Always-on-top
        self._always_on_top = False
        self.root.bind("<F2>", self._toggle_always_on_top)
        self.root.bind("<F12>", self._toggle_always_on_top)

        # UI state
        self.state = "IDLE"
        self.current_mode = "AI"

        self.status_text = tk.StringVar(value="Idle")
        self.gesture_text = tk.StringVar(value="Gestures: —")
        self.mode_text = tk.StringVar(value="AI MODE")

        self.t0 = time.time()

        # Demo mode
        self._demo_enabled = bool(DEMO_ENABLED)
        self._demo_idle_s = float(DEMO_IDLE_SECONDS)
        self._demo_every_s = float(DEMO_MESSAGE_EVERY)
        self._last_activity_ts = time.time()
        self._last_demo_msg_ts = 0.0
        self._demo_active = False
        self._demo_lines = [
            "Monitoring systems…",
            "Scanning peripherals…",
            "Calibrating sensors…",
            "Running diagnostics…",
            "Optimizing performance…",
            "Standing by.",
            "Signal stable.",
            "Thermals nominal.",
            "Network check complete.",
            "Idle loop engaged.",
        ]

        # Live preview (camera)
        self._last_preview_ts = 0.0
        self._preview_fps = 12.0
        self._preview_imgtk = None
        self._preview_last_ok = False

        # Context HUD widgets flags
        self.hud_flags = {
            "GAME": False,
            "LISTENING": False,
            "THINKING": False,
            "SPEAKING": False,
            "FACE": False,
            "ERROR": False,
        }

        # Layout
        self._build_layout()

        # Game mode button
        self.game_btn = tk.Button(
            self.root,
            text="GAME: OFF",
            command=self._toggle_game_mode,
            bd=0,
            fg=HUD_CYAN,
            bg="#07121F",
            activeforeground="#07121F",
            activebackground=HUD_CYAN,
            font=("Segoe UI", 11, "bold"),
            cursor="hand2",
        )
        self.game_btn.place(relx=0.98, rely=0.06, anchor="ne")
        self._refresh_game_button()

        self._log_line("[system] UI online. Press ESC to exit. Press F2 for always-on-top.")
        self.root.after(FPS_MS, self._ui_tick)

    # --------------------------
    # Window helpers
    # --------------------------
    def _center_window(self, w: int, h: int):
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _start_drag(self, event):
        self._drag_offset = (
            event.x_root - self.root.winfo_x(),
            event.y_root - self.root.winfo_y(),
        )

    def _do_drag(self, event):
        ox, oy = self._drag_offset
        x = event.x_root - ox
        y = event.y_root - oy
        self.root.geometry(f"+{x}+{y}")

    def _toggle_always_on_top(self, event=None):
        self._always_on_top = not self._always_on_top
        self.root.attributes("-topmost", self._always_on_top)
        self._log_line(f"[system] Always-on-top: {'ON' if self._always_on_top else 'OFF'}")
        self._touch_activity()

    # --------------------------
    # Demo mode
    # --------------------------
    def _touch_activity(self):
        self._last_activity_ts = time.time()
        self._demo_active = False

    def _demo_tick(self):
        if not self._demo_enabled:
            return
        now = time.time()

        calm = self.state in {
            "IDLE", "FACE DETECTED", "EYES OPEN", "ATTENTIVE", "LOOKING CENTER",
            "HEAD NEUTRAL", "LOOKING UP", "LOOKING DOWN"
        }
        if (now - self._last_activity_ts) >= self._demo_idle_s and calm:
            self._demo_active = True
        else:
            self._demo_active = False
            return

        if (now - self._last_demo_msg_ts) >= self._demo_every_s:
            self._last_demo_msg_ts = now
            self._log_line(f"[system] {random.choice(self._demo_lines)}")

    # --------------------------
    # Game mode
    # --------------------------
    def _toggle_game_mode(self):
        new_state = not is_game_mode()
        set_game_mode(new_state)

        if new_state:
            self.set_mode("GAME")
            self._log_line("[system] Game Mode enabled (button).")

            # NEW: auto-launch game when GAME mode is enabled
            try:
                from game_launcher import launch_game_if_needed
                ok, msg = launch_game_if_needed(self.event_q)
                if not ok:
                    self._log_line(f"[warn] {msg}")
            except Exception as e:
                self._log_line(f"[warn] Game auto-launch failed: {e}")

        else:
            self.set_mode("AI")
            self._log_line("[system] Game Mode disabled (button).")

        self._refresh_game_button()
        self._touch_activity()

    def _refresh_game_button(self):
        if is_game_mode():
            self.game_btn.config(text="GAME: ON", bg=HUD_CYAN, fg="#07121F")
        else:
            self.game_btn.config(text="GAME: OFF", bg="#07121F", fg=HUD_CYAN)

    # --------------------------
    # Layout
    # --------------------------
    def _build_layout(self):
        # Slightly cleaner top bar (same behavior)
        top = tk.Frame(self.root, bg=BG, height=46)
        top.pack(side="top", fill="x")

        # Title
        title = tk.Label(
            top,
            text=APP_TITLE,
            fg=TEXT,
            bg=BG,
            font=("Segoe UI", 12, "bold"),
        )
        title.pack(side="left", padx=14, pady=10)

        # Close button (a little nicer hover)
        self._close_btn = tk.Label(
            top,
            text="✕",
            fg=TEXT,
            bg=BG,
            font=("Segoe UI", 12, "bold"),
            cursor="hand2",
        )
        self._close_btn.pack(side="right", padx=14, pady=10)
        self._close_btn.bind("<Button-1>", lambda e: self.root.destroy())
        self._close_btn.bind("<Enter>", lambda e: self._close_btn.configure(fg=ERROR))
        self._close_btn.bind("<Leave>", lambda e: self._close_btn.configure(fg=TEXT))

        # Thin separator
        tk.Frame(self.root, bg="#0B1322", height=2).pack(side="top", fill="x")

        # Mode HUD
        self.mode_hud = tk.Label(
            self.root,
            textvariable=self.mode_text,
            fg=ACCENT,
            bg=BG,
            font=("Consolas", 11, "bold"),
            padx=10,
            pady=4
        )
        self.mode_hud.place(relx=1.0, x=-20, y=54, anchor="ne")

        main = tk.Frame(self.root, bg=BG)
        main.pack(side="top", fill="both", expand=True, padx=14, pady=10)

        left = tk.Frame(main, bg=BG)
        left.pack(side="left", fill="both", expand=True)

        right = tk.Frame(main, bg=BG, width=380)
        right.pack(side="right", fill="y")

        # Core canvas
        self.canvas = tk.Canvas(left, bg=BG, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Bottom row
        bottom = tk.Frame(left, bg=BG)
        bottom.pack(side="bottom", fill="x", pady=(8, 0))

        tk.Label(
            bottom,
            textvariable=self.status_text,
            fg=ACCENT,
            bg=BG,
            font=("Consolas", 14, "bold")
        ).pack(side="left", padx=(6, 10))

        tk.Label(
            bottom,
            textvariable=self.gesture_text,
            fg=TEXT,
            bg=BG,
            font=("Consolas", 11)
        ).pack(side="right", padx=6)

        # Right: Vision feed
        cam_title = tk.Label(right, text="VISION FEED", fg=TEXT, bg=BG, font=("Segoe UI", 10, "bold"))
        cam_title.pack(anchor="nw", pady=(6, 4))

        self.preview = tk.Label(
            right,
            bg="#02060E",
            fg=ACCENT,
            text="(no camera feed)",
            font=("Consolas", 10),
            bd=0,
            padx=8,
            pady=8
        )
        self.preview.pack(fill="x", pady=(0, 12))

        # Log title
        log_title = tk.Label(right, text="COMMAND LOG", fg=TEXT, bg=BG, font=("Segoe UI", 10, "bold"))
        log_title.pack(anchor="nw", pady=(0, 4))

        # Log container with scrollbar (better UX, no behavior changes)
        log_frame = tk.Frame(right, bg=BG)
        log_frame.pack(fill="both", expand=True)

        self.log_scroll = tk.Scrollbar(log_frame, orient="vertical")
        self.log_scroll.pack(side="right", fill="y")

        self.log = tk.Text(
            log_frame,
            height=18,
            width=42,
            bg="#02060E",
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            wrap="word",
            font=("Consolas", 10),
            yscrollcommand=self.log_scroll.set,
            padx=8,
            pady=8,
        )
        self.log.pack(side="left", fill="both", expand=True)
        self.log_scroll.config(command=self.log.yview)
        self.log.configure(state="disabled")

        # Tags
        self.log.tag_configure("system", foreground=ACCENT)
        self.log.tag_configure("user", foreground="#9BE8FF")
        self.log.tag_configure("jarvis", foreground=TEXT)
        self.log.tag_configure("error", foreground=ERROR)
        self.log.tag_configure("warn", foreground=HUD_YELLOW)

    # --------------------------
    # Logging
    # --------------------------
    def _log_line(self, line: str):
        if not line:
            return

        tag = None
        if line.startswith("[system]"):
            tag = "system"
        elif line.startswith("[user]"):
            tag = "user"
        elif line.startswith("[jarvis]"):
            tag = "jarvis"
        elif line.startswith("[error]"):
            tag = "error"
        elif line.startswith("[warn]"):
            tag = "warn"

        self.log.configure(state="normal")
        if tag:
            self.log.insert("end", line + "\n", tag)
        else:
            self.log.insert("end", line + "\n")

        # Trim old lines
        if int(self.log.index("end-1c").split(".")[0]) > LOG_LINES_MAX:
            self.log.delete("1.0", "2.0")

        self.log.see("end")
        self.log.configure(state="disabled")

    def _log_append(self, text: str, tag: str = "jarvis"):
        """Append text without newline (for streaming tokens like terminal)."""
        if not text:
            return
        self.log.configure(state="normal")
        self.log.insert("end", text, tag)
        self.log.see("end")
        self.log.configure(state="disabled")

    # --------------------------
    # State / Mode
    # --------------------------
    def set_state(self, new_state: str, message: str | None = None):
        self.state = new_state

        # Reset widget flags
        for k in self.hud_flags:
            self.hud_flags[k] = False

        # Base state mapping
        if new_state == "IDLE":
            self.status_text.set("Idle")
        elif new_state == "LISTENING":
            self.hud_flags["LISTENING"] = True
            self.status_text.set("Listening…")
        elif new_state == "THINKING":
            self.hud_flags["THINKING"] = True
            self.status_text.set("Processing…")
        elif new_state == "SPEAKING":
            self.hud_flags["SPEAKING"] = True
            self.status_text.set("Speaking…")
        elif new_state == "ERROR":
            self.hud_flags["ERROR"] = True
            self.status_text.set("Error (non-crashing)")
        else:
            # Vision state support
            self.status_text.set(new_state)
            if "FACE" in new_state.upper():
                self.hud_flags["FACE"] = True

        # Game flag comes from shared_state
        if is_game_mode():
            self.hud_flags["GAME"] = True

        if message:
            self._log_line(message)

    def set_mode(self, mode: str):
        mode = (mode or "AI").upper()
        if mode not in ("AI", "PC", "GAME"):
            self._log_line(f"[warn] Unknown mode: {mode}")
            return

        self.current_mode = mode
        self.mode_text.set(f"{mode} MODE")
        self._log_line(f"[system] Mode switched to {mode}")

    # --------------------------
    # Preview (camera)
    # --------------------------
    def _preview_tick(self):
        if not self.frame_provider:
            return

        now = time.time()
        if (now - self._last_preview_ts) < (1.0 / self._preview_fps):
            return
        self._last_preview_ts = now

        try:
            out = self.frame_provider()
        except Exception:
            return

        frame = out[0] if isinstance(out, tuple) else out
        if frame is None:
            if self._preview_last_ok:
                self.preview.config(text="(no camera feed)", image="")
                self._preview_imgtk = None
                self._preview_last_ok = False
            return

        try:
            rgb = frame[:, :, ::-1]  # BGR -> RGB
            img = Image.fromarray(rgb)
            target_w = 360
            w, h = img.size
            target_h = int(h * (target_w / w)) if w else 240
            img = img.resize((target_w, target_h))
            imgtk = ImageTk.PhotoImage(img)
        except Exception:
            return

        self._preview_imgtk = imgtk
        self.preview.config(image=imgtk, text="")
        self._preview_last_ok = True

    # --------------------------
    # Context HUD widgets
    # --------------------------
    def _draw_context_widgets(self):
        x = 36
        y = 250
        spacing = 34

        def widget(label, color):
            nonlocal y
            self.canvas.create_rectangle(x, y, x + 245, y + 26, outline=color, width=2)
            self.canvas.create_text(
                x + 10, y + 13,
                anchor="w",
                text=label,
                fill=color,
                font=("Consolas", 11, "bold")
            )
            y += spacing

        if self.hud_flags["GAME"]:
            widget("🎮 GAME MODE ACTIVE", HUD_CYAN)
        if self.hud_flags["LISTENING"]:
            widget("🎙️ LISTENING", HUD_CYAN)
        if self.hud_flags["THINKING"]:
            widget("🧠 THINKING", HUD_YELLOW)
        if self.hud_flags["SPEAKING"]:
            widget("🔊 SPEAKING", "#9BE8FF")
        if self.hud_flags["FACE"]:
            widget("👁️ FACE DETECTED", HUD_GREEN)
        if self.hud_flags["ERROR"]:
            widget("⚠️ ERROR", HUD_RED)

    # --------------------------
    # Iron-Man HUD overlay
    # --------------------------
    def _hud_panel(self, x, y, w, h, title, lines):
        self.canvas.create_rectangle(x, y, x+w, y+h, fill="#02060E", outline=HUD_ORANGE_DIM, width=2)
        self.canvas.create_text(x+10, y+14, anchor="w", text=title, fill=HUD_ORANGE,
                                font=("Consolas", 12, "bold"))
        yy = y + 38
        for line in lines[:4]:
            self.canvas.create_text(x+10, yy, anchor="w", text=line, fill=HUD_CYAN, font=("Consolas", 10))
            yy += 18

    def _draw_ironman_hud(self, t: float):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        cx, cy = w // 2, h // 2 - 20

        # Subtle grid
        step = 52
        for x in range(0, w, step):
            self.canvas.create_line(x, 0, x, h, fill=HUD_ORANGE_DIM, width=1)
        for y in range(0, h, step):
            self.canvas.create_line(0, y, w, y, fill=HUD_ORANGE_DIM, width=1)

        # Corner brackets
        pad, ln, thick = 18, 34, 3
        self.canvas.create_line(pad, pad, pad+ln, pad, fill=HUD_ORANGE, width=thick)
        self.canvas.create_line(pad, pad, pad, pad+ln, fill=HUD_ORANGE, width=thick)

        self.canvas.create_line(w-pad, pad, w-pad-ln, pad, fill=HUD_ORANGE, width=thick)
        self.canvas.create_line(w-pad, pad, w-pad, pad+ln, fill=HUD_ORANGE, width=thick)

        self.canvas.create_line(pad, h-pad, pad+ln, h-pad, fill=HUD_ORANGE, width=thick)
        self.canvas.create_line(pad, h-pad, pad, h-pad-ln, fill=HUD_ORANGE, width=thick)

        self.canvas.create_line(w-pad, h-pad, w-pad-ln, h-pad, fill=HUD_ORANGE, width=thick)
        self.canvas.create_line(w-pad, h-pad, w-pad, h-pad-ln, fill=HUD_ORANGE, width=thick)

        # Tick ring
        R = 175
        ticks = 42
        rot = (t * 40) % 360
        for i in range(ticks):
            ang = math.radians((360 / ticks) * i + rot)
            x1 = cx + (R - 10) * math.cos(ang)
            y1 = cy + (R - 10) * math.sin(ang)
            x2 = cx + (R + 10) * math.cos(ang)
            y2 = cy + (R + 10) * math.sin(ang)
            self.canvas.create_line(x1, y1, x2, y2, fill=HUD_ORANGE_DIM, width=2)

        # Sweep arc
        sweep = (t * 220) % 360
        self.canvas.create_arc(
            cx-(R+24), cy-(R+24),
            cx+(R+24), cy+(R+24),
            start=sweep, extent=65,
            style="arc", outline=HUD_ORANGE, width=4
        )

        # Scanline
        scan_y = int((sin01(t * 0.8) * (h - 60)) + 30)
        self.canvas.create_line(30, scan_y, w-30, scan_y, fill=HUD_ORANGE_DIM, width=2)

        # Side panels
        self._hud_panel(24, 110, 220, 120, "TARGETS", [
            f"MODE: {self.current_mode}",
            f"STATE: {self.state}",
            f"TOPMOST: {'ON' if self._always_on_top else 'OFF'}",
        ])
        self._hud_panel(w-244, 110, 220, 120, "FORECAST", [
            "CAM: tracking",
            "AUDIO: ready",
            "SYS: stable",
        ])

    # --------------------------
    # Core animation
    # --------------------------
    def _draw_glow_circle(self, cx, cy, r, color, width=2):
        layers = 4
        for k in range(layers, 0, -1):
            rr = r + k * 5
            self.canvas.create_oval(cx-rr, cy-rr, cx+rr, cy+rr, outline=color, width=max(1, width-1))
        self.canvas.create_oval(cx-r, cy-r, cx+r, cy+r, outline=color, width=width)

    def _draw_core(self):
        self.canvas.delete("all")

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        cx, cy = w // 2, h // 2 - 20
        t = time.time() - self.t0

        # State-based pulse
        if self.state == "IDLE":
            speed, amp = 1.2, 0.10
        elif self.state == "LISTENING":
            speed, amp = 2.2, 0.16
        elif self.state == "THINKING":
            speed, amp = 1.8, 0.20
        elif self.state == "SPEAKING":
            speed, amp = 3.4, 0.22
        elif self.state == "ERROR":
            speed, amp = 5.0, 0.06
        else:
            speed, amp = 1.3, 0.10

        pulse = 1.0 + amp * math.sin(t * speed * 2 * math.pi)
        base_r = CORE_RADIUS * pulse

        # Rings
        for i in range(RING_COUNT):
            r = base_r + (i + 1) * RING_GAP
            phase = t * speed + i * 0.6
            width = 2 + int(2 * sin01(phase * 1.7))
            color = ACCENT if self.state != "ERROR" else ERROR
            self._draw_glow_circle(cx, cy, r, color, width=width)

        # Inner core
        core_color = ACCENT if self.state != "ERROR" else ERROR
        self._draw_glow_circle(cx, cy, base_r, core_color, width=3)

        # Thinking arc
        if self.state == "THINKING":
            sweep = (t * 220) % 360
            self.canvas.create_arc(
                cx - base_r - 22, cy - base_r - 22,
                cx + base_r + 22, cy + base_r + 22,
                start=sweep, extent=70,
                style="arc", outline=ACCENT, width=3
            )

        # Listening ears
        if self.state == "LISTENING":
            ear = 18 + 8 * sin01(t * 7.0)
            self.canvas.create_line(cx - base_r - 26, cy, cx - base_r - 26, cy - ear, fill=ACCENT, width=3)
            self.canvas.create_line(cx + base_r + 26, cy, cx + base_r + 26, cy - ear, fill=ACCENT, width=3)

        # Crosshair
        self.canvas.create_line(cx-14, cy, cx+14, cy, fill=ACCENT_DIM, width=1)
        self.canvas.create_line(cx, cy-14, cx, cy+14, fill=ACCENT_DIM, width=1)

        # Overlays
        self._draw_ironman_hud(t)
        self._draw_context_widgets()

    # --------------------------
    # Event loop
    # --------------------------
    def _consume_events(self):
        got_any = False
        while True:
            try:
                ev: UiEvent = self.event_q.get_nowait()
            except Empty:
                break

            got_any = True

            if ev.type == "state":
                if self.on_state_callback:
                    try:
                        self.on_state_callback(ev.payload.get("state", ""))
                    except Exception:
                        pass
                self.set_state(ev.payload.get("state", "IDLE"), ev.payload.get("log"))

            elif ev.type == "log":
                self._log_line(ev.payload.get("text", ""))

            elif ev.type == "stream":
                # NEW: terminal-like streaming output
                self._log_append(ev.payload.get("text", ""), ev.payload.get("tag", "jarvis"))

            elif ev.type == "gesture":
                self.gesture_text.set(f"Gestures: {ev.payload.get('text', '—')}")

            elif ev.type == "mode":
                self.set_mode(ev.payload.get("mode", "AI"))

        if got_any:
            self._touch_activity()

        self._refresh_game_button()

    def _ui_tick(self):
        self._consume_events()
        self._demo_tick()
        self._preview_tick()
        self._draw_core()
        self.root.after(FPS_MS, self._ui_tick)

    # --------------------------
    # Run
    # --------------------------
    def run(self):
        self.root.mainloop()