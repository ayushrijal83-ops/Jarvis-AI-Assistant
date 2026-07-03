# utils.py
from __future__ import annotations
import math
import time
from dataclasses import dataclass

def now_ms() -> int:
    return int(time.time() * 1000)

def clamp(x: float, a: float, b: float) -> float:
    return max(a, min(b, x))

def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t

def ease_in_out(t: float) -> float:
    # smoothstep
    t = clamp(t, 0.0, 1.0)
    return t * t * (3 - 2 * t)

def sin01(x: float) -> float:
    return (math.sin(x) + 1.0) / 2.0

@dataclass
class UiEvent:
    type: str
    payload: dict
