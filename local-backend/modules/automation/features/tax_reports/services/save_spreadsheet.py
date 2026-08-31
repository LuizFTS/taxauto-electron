import os
import time
from time import sleep

import nazm as a
import nazm.capture as c
import pyperclip

from modules.automation.features.tax_reports.utils.change_spreadsheet_filename import (
    change_spreadsheet_filename,
)
from modules.automation.infrastructure.erp_session import ERPSession


class SaveSpreadsheet:
    def __init__(self, session: ERPSession, state):
        self.session = session
        self.state = state
        self.t = c.load_templates()

    def execute(self, company, book_type, start_date, end_date, first_round) -> str | None:
        if first_round:
            self.state.check()

        base_name = f"{company}_{book_type.upper()}"
        unique_folder_name = f"{base_name}_{int(time.time())}"

        base_dir = os.getenv("LOCALAPPDATA")

        if base_dir is None:
            raise Exception("Nenhum diretório de armazenamento encontrado.")
        else:
            root_temp_dir = os.path.join(base_dir, "TaxAuto", "Temp")

        os.makedirs(root_temp_dir, exist_ok=True)
        specific_temp_dir = os.path.join(root_temp_dir, unique_folder_name)
        os.makedirs(specific_temp_dir, exist_ok=True)

        # Create a temp dir to save this spreadsheet for now
        # stringfy temp_dir
        company = str(int(company))

        # Fill company field
        a.type(company)
        a.press("tab")
        self.state.check()

        # Leave branch field empty
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
            a.press("tab", 8)
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
        sleep(1)

        # Fill save path in save dialog
        a.wait_for(self.t.dialog_ok)
        pyperclip.copy(specific_temp_dir)
        self.state.check()
        a.double_press("ctrl", "v")
        a.press("tab", 2)
        a.press("space")
        self.state.check()

        # Press ok to finish
        a.wait_for(self.t.alert_icon)
        new_file_path = change_spreadsheet_filename(specific_temp_dir, base_name)
        a.press("space")
        self.state.check()

        sleep(0.5)
        self.state.check()
        a.press("tab", 3)
        self.state.check()

        return new_file_path if new_file_path else None
