from time import sleep

import nazm as a
import nazm.capture as c


class OpenBookService:

    def __init__(self, state):
        self.state = state

    def execute(self):
        t = c.load_templates()
        print("[SERVICE] OPEN BOOK")

        # a.click(t.binoculos, 1017, 160)
        a.click(t.unlock_icon)
        self.state.check()
        a.press("tab")
        self.state.check()
        a.press("space")
        self.state.check()
        sleep(0.5)
