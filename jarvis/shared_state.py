# shared_state.py
import threading

_lock = threading.Lock()
_game_mode = False

def set_game_mode(enabled: bool) -> None:
    global _game_mode
    with _lock:
        _game_mode = bool(enabled)

def is_game_mode() -> bool:
    with _lock:
        return _game_mode
