import tkinter as tk
import threading

class Overlay:
    def __init__(self):
        self.root = None
        self.label = None
        self._ready = threading.Event()
        self._drag_x = 0
        self._drag_y = 0

    def run(self):
        self.root = tk.Tk()

        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.92)
        self.root.configure(bg="#1e1e1e")
        self.root.withdraw()

        self.label = tk.Label(
            self.root,
            text="",
            font=("Segoe UI", 13),
            fg="#a0a0a0",
            bg="#1e1e1e",
            padx=14,
            pady=8,
        )
        self.label.pack()

        # ── drag bindings ─────────────────────────────────────────
        self.label.bind("<ButtonPress-1>",   self._on_drag_start)
        self.label.bind("<B1-Motion>",       self._on_drag_motion)

        self._ready.set()
        self.root.mainloop()

    # ── drag handlers ─────────────────────────────────────────────
    def _on_drag_start(self, event):
        """Record where the mouse clicked relative to the window."""
        self._drag_x = event.x
        self._drag_y = event.y

    def _on_drag_motion(self, event):
        """Move the window as the mouse drags."""
        x = self.root.winfo_x() + (event.x - self._drag_x)
        y = self.root.winfo_y() + (event.y - self._drag_y)
        self.root.geometry(f"+{x}+{y}")

    # ── position ──────────────────────────────────────────────────
    def _position_window(self):
        """Default position — bottom right. Only used on first show."""
        self.root.update_idletasks()

        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        win_w    = self.root.winfo_width()
        win_h    = self.root.winfo_height()

        x = screen_w - win_w - 24
        y = screen_h - win_h - 64

        self.root.geometry(f"+{x}+{y}")

    # ── show / hide ───────────────────────────────────────────────
    def show(self, suggestion: str):
        self._ready.wait()

        def _show():
            self.label.config(text=f"  {suggestion}  ")

            # only auto-position on first show
            # after that, stay where the user dragged it
            if self.root.winfo_x() == 0 and self.root.winfo_y() == 0:
                self._position_window()

            self.root.deiconify()
            self.root.lift()

        self.root.after(0, _show)

    def hide(self):
        self._ready.wait()

        def _hide():
            self.root.withdraw()

        self.root.after(0, _hide)