import time
import threading
import keyboard

def run_key_handler(hotkey: str, on_accept, create_suggestion):
    """
    Start a global hotkey listener.
    Blocks the calling thread - run in a daemon thread from main.py
    """
    idle_timer: threading.Timer | None = None

    def on_press(e):
        on_accept()

    def on_idle():
        global next_phrase

        create_suggestion()

    def reset_idle_timer(e):
        nonlocal idle_timer
        if e.name == 'tab':
            return
        if idle_timer is not None:
            idle_timer.cancel()
        idle_timer = threading.Timer(0.1, on_idle)
        idle_timer.start()

    keyboard.on_press_key(hotkey, on_press, suppress=True)
    keyboard.on_press(reset_idle_timer)
    keyboard.wait()
