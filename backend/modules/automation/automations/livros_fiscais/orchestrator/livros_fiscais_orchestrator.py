from modules.automation.automations.livros_fiscais.navigation.erp_session import ERPSession
from modules.automation.automations.livros_fiscais.navigation.navigate_to_livros_fiscais import (
    NavigateToLivrosFiscais,
)
from modules.automation.automations.livros_fiscais.orchestrator.save_books_orchestrator import (
    SaveBooksOrchestrator,
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

        self.save_book = SaveBooksOrchestrator()

    def execute(self, dto):
        print("[ORCHESTRATOR] Starting Livros Fiscais automation")
        # self.session.open()

        # self.navigator.execute()

        for filial in dto.filiais:
            print(f"[ORCHESTRATOR] Processing filial {filial}")
            is_open = self.book_state.is_open(dto.book_type, filial, dto.start_date)
            print("teste 2")

            if is_open:

                if dto.tasks.update_book:
                    self.update_book.execute()

                if dto.tasks.close_book:
                    self.close_book.execute()

            else:
                print("teste")

                if dto.tasks.open_book:
                    self.open_book.execute()

                if dto.tasks.update_book:
                    self.update_book.execute()

                if dto.tasks.close_book:
                    self.close_book.execute()

        if dto.tasks.save_spreadsheet or dto.tasks.save_pdf:
            orchestrator = SaveBooksOrchestrator()
            orchestrator.execute(dto)

        return {"status": "finished"}
