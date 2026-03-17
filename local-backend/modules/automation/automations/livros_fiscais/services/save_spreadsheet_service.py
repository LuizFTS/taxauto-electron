from time import sleep

import nazm as a
import nazm.capture as c
import pyperclip

from modules.automation.automations.livros_fiscais.navigation.erp_session import ERPSession
from modules.automation.automations.livros_fiscais.utils.change_spreadsheet_filename import (
    change_spreadsheet_filename,
)


class SaveSpreadsheetService:
    def __init__(self, session: ERPSession, state):
        self.session = session
        self.state = state
        self.t = c.load_templates()

    def execute(self, filial, book_type, start_date, end_date, save_path, first_round):
        company = "2" if int(filial) >= 70 else "1"

        if first_round:
            self.state.check()

        # Fill company field
        a.type(company)
        a.press("tab")
        self.state.check()

        # Fill branch field
        a.type(str(int(filial)))
        a.press("tab")
        self.state.check()

        # Select book type
        if book_type == "entrada":
            a.press("down")
            a.press("tab")
            self.state.check()
            if first_round:
                a.press("space")
            a.press("tab", 4)
            self.state.check()
            a.press("up")
            a.press("tab")
            a.press("up")
            a.press("tab", 7)
            self.state.check()
            a.press("up")
            a.press("tab", 3)

        if book_type == "saida":
            a.press("tab", 10)
            self.state.check()
            a.press("up")
            a.press("tab", 3)
        self.state.check()

        if first_round:
            a.type(start_date)
        self.state.check()
        a.press("tab")
        self.state.check()
        if first_round:
            a.type(end_date)
        self.state.check()

        # Open save spreadsheet dialog
        a.press("tab", 2)
        a.press("space")
        self.state.check()

        # Fill save path in save dialog
        a.wait_for(self.t.dialog_ok)
        pyperclip.copy(save_path)
        self.state.check()
        a.double_press("ctrl", "v")
        a.press("tab", 2)
        a.press("space")
        self.state.check()

        # Press ok to finish
        a.wait_for(self.t.alert_icon)
        a.press("space")
        self.state.check()

        sleep(0.5)
        self.state.check()
        a.press("tab", 2)
        self.state.check()

        change_spreadsheet_filename(save_path, f"{str(filial).zfill(2)}_{book_type.upper()}.csv")

        self.state.check()
