import nazm as a
import nazm.capture as c


class CloseBookService:
    def __init__(self, state):
        self.state = state

    def execute(self):
        t = c.load_templates()
        print("[SERVICE] CLOSE BOOK |")

        # a.click(t.binoculos, 965, 163)
        a.click(t.lock_icon)
        self.state.check()
        a.press("tab")
        self.state.check()
        a.wait_cursor_normal()
        self.state.check()
        a.press("space")
        self.state.check()
