import nazm as a
import nazm.capture as c


class OpenBookService:

    def execute(self):
        t = c.load_templates()
        print("[SERVICE] OPEN BOOK")

        a.click(t.binoculos, 1017, 160)
        a.press('tab')
        a.press('space')
        
