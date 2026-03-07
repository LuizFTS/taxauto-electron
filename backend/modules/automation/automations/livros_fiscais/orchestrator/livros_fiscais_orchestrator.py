from modules.automation.automations.livros_fiscais.navigation.erp_session import ERPSession
from modules.automation.automations.livros_fiscais.navigation.navigate_to_livros_fiscais import (
    NavigateToLivrosFiscais,
)
from modules.automation.automations.livros_fiscais.services.close_book_service import (
    CloseBookService,
)
from modules.automation.automations.livros_fiscais.services.open_book_service import OpenBookService
from modules.automation.automations.livros_fiscais.services.refresh_book_service import (
    RefreshBookService,
)
from modules.automation.automations.livros_fiscais.state.book_state_service import BookStateService


class LivrosFiscaisOrchestrator:
    def __init__(self):

        self.session = ERPSession()
    
        self.navigator = NavigateToLivrosFiscais()

        self.book_state = BookStateService()

        self.open_book = OpenBookService()
        self.refresh_book = RefreshBookService()
        self.close_book = CloseBookService()

    def execute(self, dto):
        print("[ORCHESTRATOR] Starting Livros Fiscais automation")
        self.session.open()

        self.navigator.execute(self.session)

        for filial in dto.filiais:
            print(f"[ORCHESTRATOR] Processing filial {filial}")
            is_open = self.book_state.is_open(
                self.session,
                filial,
                dto.book_type
            )

            if is_open:

                if dto.tasks.refresh_book:
                    self.refresh_book.execute(
                        self.session,
                        filial,
                        dto.book_type,
                        dto.start_date,
                        dto.end_date
                    )

                if dto.tasks.close_book:
                    self.close_book.execute(
                        self.session,
                        filial,
                        dto.book_type,
                        dto.start_date,
                        dto.end_date
                    )

            else:

                if dto.tasks.open_book:
                    self.open_book.execute(
                        self.session,
                        filial,
                        dto.book_type,
                        dto.start_date,
                        dto.end_date
                    )

                if dto.tasks.refresh_book:
                    self.refresh_book.execute(
                        self.session,
                        filial,
                        dto.book_type,
                        dto.start_date,
                        dto.end_date
                    )

                if dto.tasks.close_book:
                    self.close_book.execute(
                        self.session,
                        filial,
                        dto.book_type,
                        dto.start_date,
                        dto.end_date
                    )

        return {"status": "finished"}