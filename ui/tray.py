import pystray
from PIL import Image, ImageDraw
from threading import Event

# -- Icon drawing
def _create_icon(running: bool) -> Image.Image:
    """
    Draw a simple circle icon.
    Green = running, gray = paused.
    """
    size = 64
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    color = (80, 200, 120) if running else (150, 150, 150)
    draw.ellipse([8, 8, size - 8, size - 8], fill=color)

    return image


# -- Tray class
class Tray:
    def __init__(self, on_toggle):
        self.on_toggle = on_toggle
        self.running = True
        self._icon = None

    def _build_menu(self) -> pystray.Menu:
        return pystray.Menu(
            pystray.MenuItem(
                lambda text: "Pause" if self.running else "Resume",
                self._toggle,
                default=False,
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit", self._quit),
        )

    def _toggle(self, icon, item):
        self.running = not self.running
        self.on_toggle(self.running)

        # update icon color and menu label
        icon.icon  = _create_icon(self.running)
        icon.title = "GhostText - Running" if self.running else "GhostText - Paused"
        icon.update_menu()

    def _quit(self, icon, item):
        print("[tray] Quitting")
        icon.stop()

    def run(self):
        """Blocks the main thread - app lives here."""
        print("[tray] Starting")

        self._icon = pystray.Icon(
            name="ghosttext",
            icon=_create_icon(self.running),
            title="GhostText — Running",
            menu=self._build_menu(),
        )

        self._icon.run()