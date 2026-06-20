from time import sleep

import nazm as a
import nazm.capture as c


class CloseBook:
    def __init__(self, state):
        self.state = state

    def execute(self):
        t = c.load_templates()
        print("[SERVICE] CLOSE BOOK |")

        sleep(1)
        a.click(t.lock_icon)
        self.state.check()
        a.press("tab")
        self.state.check()
        a.wait_cursor_normal()
        self.state.check()
        sleep(0.3)
        a.press("space")
        self.state.check()
        sleep(0.5)
