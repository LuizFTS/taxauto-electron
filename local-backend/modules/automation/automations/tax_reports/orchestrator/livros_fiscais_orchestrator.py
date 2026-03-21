import nazm as a

from modules.automation.automations.state.automation_state import AutomationState
from modules.automation.automations.tax_reports.navigation.erp_session import ERPSession
from modules.automation.automations.tax_reports.navigation.navigate_to_livros_fiscais import (
    NavigateToLivrosFiscais,
)
from modules.automation.automations.tax_reports.orchestrator.save_books_orchestrator import (
    SaveBooksOrchestrator,
)
from modules.automation.automations.tax_reports.services.close_book_service import (
    CloseBookService,
)
from modules.automation.automations.tax_reports.services.open_book_service import OpenBookService
from modules.automation.automations.tax_reports.services.update_book_service import (
    UpdateBookService,
)
from modules.automation.automations.tax_reports.state.book_state_service import BookStateService


class LivrosFiscaisOrchestrator:
    def __init__(self, state: AutomationState):
        self.state = state

        self.session = ERPSession()

        self.navigator = NavigateToLivrosFiscais()

        self.book_state = BookStateService()

        self.open_book = OpenBookService(self.state)
        self.update_book = UpdateBookService(self.state)
        self.close_book = CloseBookService(self.state)

    def execute(self, dto):
        print("[ORCHESTRATOR] Starting Livros Fiscais automation")
        self.state.check()

        self.session.open()
        self.state.check()

        self.navigator.execute()
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

                if dto.tasks.close_book:
                    self.state.check()
                    self.close_book.execute()

        self.state.check()

        if dto.tasks.save_spreadsheet or dto.tasks.save_pdf:
            orchestrator = SaveBooksOrchestrator(self.session, self.state)
            orchestrator.execute(dto)

        self.state.check()
        a.double_press("ctrl", "q")
        return {"status": "finished"}
