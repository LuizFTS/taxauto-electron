import nazm as a

from modules.automation.application.dto.tax_reports_dto import TaxReportsDTO
from modules.automation.features.state.automation_state import AutomationState
from modules.automation.features.tax_reports.navigation import (
    Navigation,
)
from modules.automation.infrastructure.erp_session import ERPSession


class TaxReportsOrchestrator:
    def __init__(
        self,
        state: AutomationState,
        navigator: Navigation,
        session: ERPSession,
    ):
        self.state = state
        self.session = session
        self.navigator = navigator

    def _get_erp_module(self, module: str) -> str:
        if module == "ICAN":
            return "OBFI3090"

        if module == "ICST_NFE":
            return "OBFI2190"

        if module == "ICST_CTE":
            return "OBFI2510"

        if module == "ESTORNOS":
            return "OBFI1230"

        if module == "FRETE":
            return "OBFI2720"

        if module == "DIFAL_NFE":
            return "OBFI4110"

        if module == "DIFAL_CTE":
            return "OBFI4120"

        if module == "FOT":
            return "OBFI2200"
        return ""

    def execute(self, dto: TaxReportsDTO):
        print("[ORCHESTRATOR] Starting Livros Fiscais automation")
        self.state.check()

        self.session.open()
        self.state.check()

        self.navigator.execute(self._get_erp_module(dto.module))
        self.state.check()

        if dto.tasks.open_book or dto.tasks.update_book or dto.tasks.close_book:
            for filial in dto.filiais:
                self.state.check()

                print(f"[ORCHESTRATOR] Processing filial {filial}")
                is_open = self.book_state.is_open(dto.book_type, filial, dto.start_date)

                necessita_abrir = not is_open and (dto.tasks.open_book or dto.tasks.update_book)
                self.state.check()

                if necessita_abrir:
                    self.state.check()
                    self.open_book.execute()

                if dto.tasks.update_book:
                    self.state.check()
                    self.update_book.execute()

                # Close book if the book is open or if the book was opened in this execution
                if dto.tasks.close_book and (
                    is_open or dto.tasks.open_book or dto.tasks.update_book
                ):
                    self.state.check()
                    self.close_book.execute()

        if (dto.tasks.open_book or dto.tasks.update_book or dto.tasks.close_book) and (
            not dto.tasks.save_spreadsheet and not dto.tasks.save_pdf
        ):
            a.double_press("ctrl", "q")

        self.state.check()

        if dto.tasks.save_spreadsheet or dto.tasks.save_pdf:
            self.save_books.execute(dto)

        self.state.check()
        return {"status": "finished"}
