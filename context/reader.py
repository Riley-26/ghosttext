import ctypes
import uiautomation as auto

def get_context():
    """Find the currently focused input element and return its text, or None if unavailable."""
    ctypes.windll.ole32.CoInitialize(None)
    try:
        focused = auto.GetFocusedControl()
        return focused.GetValuePattern().Value
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        ctypes.windll.ole32.CoUninitialize()