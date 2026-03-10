import nazm as a
import nazm.capture as c


class UpdateBookService:

    def execute(self):
        t = c.load_templates()
        print("[SERVICE] UPDATE BOOK |")

        a.click(t.binoculos, 969, 101)

        a.wait_cursor_normal()

        a.press('left')
        a.press('space')

        a.wait_cursor_normal()

        a.press('enter')