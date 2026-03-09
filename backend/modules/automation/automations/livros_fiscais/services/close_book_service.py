import nazm as a
import nazm.capture as c

class CloseBookService:

    def execute(self):
        t = c.load_templates()
        print("[SERVICE] CLOSE BOOK |")

        a.click(t.binoculos, 965, 163)
        a.press('tab')
        a.wait_cursor_normal()
        a.press('space')