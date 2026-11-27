from pathlib import Path
from time import sleep

import nazm as a
import nazm.capture as c
import pyperclip


class Difal_cte:
    """def __init__(self, state):
    self.state = state"""

    def execute(self, company, start_date, end_date, path):
        t = c.load_templates()
        print("[SERVICE] DIFAL CTE |")

        path = Path(path).parent

        sleep(2)

        # Empresa
        a.type(str(company))

        # Pular filial
        a.press("tab", 2)

        # Selecionar "Débito e Crédito"
        a.press("down")

        # Preencher data inicial
        a.press("tab")
        a.type(start_date)

        # Preencher data final
        a.press("tab")
        a.type(end_date)

        pyperclip.copy(path)
        # Exportar excel
        a.press("tab", 2)
        a.press("space")
        a.press("tab")
        a.press("space")

        a.wait_for(t.dialog_ok)
        a.double_press("ctrl", "v")
        a.press("tab", 2)
        a.press("space")

        a.click(t.ok)
        a.press("space")
        a.press("space")
        sleep(1)
        a.double_press("ctrl", "q")


""" exec = Difal_cte()
exec.execute(1, "01092026", "19092026", "C:\\Users\\lu9887091\\Downloads\\Nova pasta (3)\\01") """
