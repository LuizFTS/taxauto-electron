from time import sleep

import nazm as a
import nazm.capture as c


class OpenBook:
    def __init__(self, state):
        self.state = state

    def execute(self):
        t = c.load_templates()
        print("[SERVICE] OPEN BOOK")

        sleep(1)
        a.click(t.unlock_icon)
        self.state.check()
        a.press("tab")
        self.state.check()
        sleep(1)
        a.press("space")
        self.state.check()
        sleep(0.5)
