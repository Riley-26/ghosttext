import time
import threading
import keyboard

IDLE_TIME = 0.3

def run_key_handler(accept_hotkey: str, cancel_hotkey: str, accept_sug, cancel_sug, create_suggestion):
    """
    Start a global hotkey listener.
    Blocks the calling thread - run in a daemon thread from main.py
    """
    idle_timer: threading.Timer | None = None
    must_suppress = False    # Starts as false as there is no suggestion
    accept_hook = None

    def register_accept_hook():
        nonlocal accept_hook
        if accept_hook is not None:
            keyboard.unhook(accept_hook)
        accept_hook = keyboard.on_press_key(accept_hotkey, on_accept_key, suppress=must_suppress)

    def on_cancel_key(e):
        nonlocal must_suppress
        must_suppress = False
        cancel_sug()
        register_accept_hook()

    def on_accept_key(e):
        nonlocal must_suppress
        must_suppress = False
        accept_sug()

    def on_idle():
        nonlocal must_suppress
        must_suppress = True   # Suppress when user has been idle, so it doesn't insert the hotkey
        create_suggestion()
        register_accept_hook()

    def reset_idle_timer(e):
        nonlocal idle_timer
        if e.name == 'tab':
            return
        if idle_timer is not None:
            idle_timer.cancel()
        idle_timer = threading.Timer(IDLE_TIME, on_idle)
        idle_timer.start()

    register_accept_hook()
    keyboard.on_press_key(cancel_hotkey, on_cancel_key, suppress=True)

    keyboard.on_press(reset_idle_timer)
    keyboard.wait()
