# main.py                                               
from __future__ import annotations

from queue import Queue
from utils import UiEvent


def main():
    event_q: "Queue[UiEvent]" = Queue()

    # 1) Voice
    from voice import VoiceManager
    vm = VoiceManager(event_q)
    vm.start()

    # 2) GestureManager MUST start before UI preview (camera owner)
    from gesture import GestureManager
    gm = GestureManager(event_q)
    gm.start()

    # 3) UI (gets frames from gm)
    from ui import JarvisUI
    ui = JarvisUI(
        event_q,
        on_state_callback=vm.on_vision_state,
        frame_provider=gm.get_latest_frame,  # returns (frame, ts)
    )

    # 4) Gesture game driver (run in background)
    gdriver = None
    try:
        import threading
        from gesture_control import GestureGameDriver
        gdriver = GestureGameDriver(gm, event_q)      
        threading.Thread(target=gdriver.start, daemon=True).start()
    except Exception as e:
        event_q.put(UiEvent(type="log", payload={"text": f"[warn] GestureGameDriver not started: {e}"}))

    # 5) Vision (uses gm frames)
    vision = None
    try:
        from vision import VisionManager
        vision = VisionManager(event_q, gm)
        vision.start()
    except Exception as e:
        event_q.put(UiEvent(type="log", payload={"text": f"[warn] VisionManager not started: {e}"}))

    # 6) Run UI
    try:
        ui.run()
    finally:
        try:
            if vision:            
                vision.stop()
        except Exception:
            pass   
        try:
            if gdriver:
                gdriver.stop()
        except Exception:
            pass
        try:
            gm.stop()                                  
        except Exception:
            pass
        try:
            vm.stop()
        except Exception:
            pass


if __name__ == "__main__":
    main()
      