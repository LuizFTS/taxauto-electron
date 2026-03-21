import nazm as a
import nazm.capture as c


class UpdateBookService:
    def __init__(self, state):
        self.state = state

    def execute(self):
        t = c.load_templates()
        print("[SERVICE] UPDATE BOOK |")

        # a.click(t.binoculos, 969, 101)
        a.click(t.update)
        self.state.check()

        a.wait_cursor_normal()

        a.press("left")
        a.press("space")
        self.state.check()

        a.wait_cursor_normal()

        a.press("enter")
        self.state.check()
