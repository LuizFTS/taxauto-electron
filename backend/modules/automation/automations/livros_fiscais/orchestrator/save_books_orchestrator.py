from modules.automation.automations.livros_fiscais.navigation.erp_session import ERPSession
from modules.automation.automations.livros_fiscais.services.save_pdf_service import SavePDFService
from modules.automation.automations.livros_fiscais.services.save_spreadsheet_service import (
    SaveSpreadsheetService,
)


class SaveBooksOrchestrator:
    def __init__(self):

        self.session = ERPSession()

        self.save_pdf = SavePDFService()
        self.save_spreadsheet = SaveSpreadsheetService()

    def execute(self, dto):

        print("[ORCHESTRATOR] Starting saving books automation")
        # self.session.open()

        # self.navigator.execute()

        for filial in dto.filiais:
            print(f"[ORCHESTRATOR] Processing filial {filial}")

            if dto.tasks.save_pdf:
                self.save_pdf.execute(
                    filial=filial,
                    book_type=dto.book_type,
                    start_date=dto.start_date,
                    end_date=dto.end_date,
                )

            if dto.tasks.save_spreadsheet:
                self.save_spreadsheet.execute(
                    filial=filial,
                    book_type=dto.book_type,
                    start_date=dto.start_date,
                    end_date=dto.end_date,
                )
