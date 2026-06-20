from time import sleep

import nazm as a
import nazm.capture as c


class UpdateBook:
    def __init__(self, state):
        self.state = state

    def execute(self):
        t = c.load_templates()
        print("[SERVICE] UPDATE BOOK |")

        sleep(1)
        a.click(t.update)
        self.state.check()

        a.wait_cursor_normal()

        a.press("left")
        sleep(0.3)
        a.press("space")
        self.state.check()

        a.wait_cursor_normal()

        a.press("enter")
        self.state.check()
        sleep(0.5)
