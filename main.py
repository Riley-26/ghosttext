import threading
import yaml
import keyboard
from config.loader import load_config
from context.reader import get_context
from inference.ollama import get_llm_response
from key_listener import run_key_handler
from ui.tray import Tray
from ui.overlay import Overlay

current_suggestion = ""
overlay = None
is_running = True


def create_suggestion():
    """Called after the user is idle for a second."""
    global current_suggestion

    if not is_running:
        return

    # 1. Get context from whatever app is focused
    context = get_context()
    if not context:
        return

    # 2. Build prompt and get suggestion from ollama
    suggestion = get_llm_response(context)
    if not suggestion:
        return

    # 3. store and show in overlay
    print(suggestion)
    current_suggestion = suggestion
    overlay.show(suggestion)


def accept_sug():
    """Called when the user presses the accept hotkey."""
    global current_suggestion

    if not current_suggestion or not is_running:
        return

    # Small delay so overlay hides before injection
    threading.Timer(0.05, inject_suggestion).start()


def cancel_sug():
    """Called when the user presses the cancel hotkey."""
    global current_suggestion
    
    current_suggestion = ""
    overlay.show("")


def inject_suggestion():
    from injector import inject
    global current_suggestion

    inject(current_suggestion)
    current_suggestion = ""
    overlay.show("")


def on_toggle(running: bool):
    """Called when the user toggles run/pause from the tray."""
    global is_running
    is_running = running
    if not running:
        overlay.hide()


# -- Runner
def main():
    global overlay

    config = load_config("config/config.yaml")

    # Start overlay (runs in its own thread)
    overlay = Overlay()
    overlay_thread = threading.Thread(target=overlay.run, daemon=True)
    overlay_thread.start()

    overlay.show("")

    hotkey_thread = threading.Thread(
        target=run_key_handler,
        args=(
            config["hotkey_accept"],
            config["hotkey_cancel"],
            accept_sug,
            cancel_sug,
            create_suggestion
        ),
        daemon=True
    )
    hotkey_thread.start()

    # Tray blocks the main thread - app lives here
    tray = Tray(on_toggle=on_toggle)
    tray.run()


if __name__ == "__main__":
    main()