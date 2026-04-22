import keyboard
import time

def inject(text: str) -> None:
    """
    Types the suggestion into the currently focused field.
    Called after the user presses the accept hotkey.
    """
    if not text or not text.strip():
        print("[injector] Empty suggestion, skipping")
        return

    text = text.strip()
    print(f"[injector] Injecting: '{text}'")

    for char in text:
        keyboard.write(char)
        time.sleep(0.02)  # 50ms between keystrokes - adjust as needed