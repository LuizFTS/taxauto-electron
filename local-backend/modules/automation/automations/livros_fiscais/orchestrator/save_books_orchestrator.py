import os
from pathlib import Path

import nazm as a
import nazm.capture as c

from modules.automation.automations.livros_fiscais.navigation.erp_session import ERPSession
from modules.automation.automations.livros_fiscais.services.merge_books_service import (
    MergeBooksService,
)
from modules.automation.automations.livros_fiscais.services.save_pdf_service import SavePDFService
from modules.automation.automations.livros_fiscais.services.save_spreadsheet_service import (
    SaveSpreadsheetService,
)


class SaveBooksOrchestrator:
    def __init__(self, session: ERPSession, state):
        self.state = state
        self.session = session

        self.save_pdf = SavePDFService(self.session, self.state)
        self.save_spreadsheet = SaveSpreadsheetService(self.session, self.state)
        self.merge_books = MergeBooksService()

    def execute(self, dto):

        print("[ORCHESTRATOR] Starting saving books automation")
        t = c.load_templates()

        a.click(t.livro_printer)
        self.state.check()
        a.wait_cursor_normal()

        first_round = True
        excel_paths = []

        for filial in dto.filiais:
            print(f"[ORCHESTRATOR] Processing filial {filial}")
            self.state.check()

            file_name = f"{str(filial).zfill(2)}_{dto.book_type.upper()}"
            pdf_path = Path(dto.save_path) / f"{file_name}.pdf"
            spreadsheet_path = Path(dto.save_path)

            if dto.tasks.save_pdf:

                self.save_pdf.execute(
                    filial=filial,
                    book_type=dto.book_type,
                    start_date=dto.start_date,
                    end_date=dto.end_date,
                    save_path=str(pdf_path),
                    first_round=first_round,
                )
            self.state.check()

            if dto.tasks.save_spreadsheet:
                self.save_spreadsheet.execute(
                    filial=filial,
                    book_type=dto.book_type,
                    start_date=dto.start_date,
                    end_date=dto.end_date,
                    save_path=str(spreadsheet_path),
                    first_round=first_round,
                )
                new_path = os.path.join(
                    str(spreadsheet_path),
                    f"{str(filial).zfill(2)}_{dto.book_type.upper()}.csv",
                )

                excel_paths.append(new_path)

            first_round = False
            self.state.check()

        if dto.tasks.save_spreadsheet and dto.consolidado:
            self.merge_books.execute(excel_paths, dto.book_type)

        a.double_press("ctrl", "q")
