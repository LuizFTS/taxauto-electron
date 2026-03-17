import keyboard


class AutomationStoppedException(Exception):
    """Raised when user interrupts the automation."""

    pass


class AutomationState:

    def __init__(self):
        self._stop_requested = False
        self._register_hotkey()

    def _register_hotkey(self):
        keyboard.add_hotkey("esc", self.request_stop)

    def request_stop(self):
        print("ESC pressed — stopping automation...")
        self._stop_requested = True

    def reset(self):
        self._stop_requested = False

    def check(self):
        if self._stop_requested:
            raise AutomationStoppedException("Automation stopped by user")
