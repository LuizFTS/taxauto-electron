from modules.automation.automations.livros_fiscais.navigation.erp_session import ERPSession
from modules.automation.automations.livros_fiscais.navigation.navigate_to_livros_fiscais import (
    NavigateToLivrosFiscais,
)
from modules.automation.automations.livros_fiscais.services.close_book_service import (
    CloseBookService,
)
from modules.automation.automations.livros_fiscais.services.open_book_service import OpenBookService
from modules.automation.automations.livros_fiscais.services.update_book_service import (
    UpdateBookService,
)
from modules.automation.automations.livros_fiscais.state.book_state_service import BookStateService


class LivrosFiscaisOrchestrator:
    def __init__(self):

        self.session = ERPSession()

        self.navigator = NavigateToLivrosFiscais()

        self.book_state = BookStateService()

        self.open_book = OpenBookService()
        self.update_book = UpdateBookService()
        self.close_book = CloseBookService()

    def execute(self, dto):
        print("[ORCHESTRATOR] Starting Livros Fiscais automation")
        # self.session.open()

        # self.navigator.execute()

        for filial in dto.filiais:
            print(f"[ORCHESTRATOR] Processing filial {filial}")
            is_open = self.book_state.is_open(dto.book_type, filial, dto.start_date)

            if is_open:

                if dto.tasks.update_book:
                    self.update_book.execute()

                if dto.tasks.close_book:
                    self.close_book.execute()

            else:

                if dto.tasks.open_book:
                    self.open_book.execute()

                if dto.tasks.update_book:
                    self.update_book.execute()

                if dto.tasks.close_book:
                    self.close_book.execute()

        return {"status": "finished"}
