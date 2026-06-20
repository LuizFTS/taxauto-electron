import nazm as a

from modules.automation.features.merge_excel_files.merge_excel_files_service import (
    MergeExcelFilesService,
)
from modules.automation.features.state.automation_state import AutomationState
from modules.automation.features.tax_reports.navigation import (
    Navigation,
)
from modules.automation.features.tax_reports.orchestrator.save_books_orchestrator import (
    SaveBooksOrchestrator,
)
from modules.automation.features.tax_reports.services.close_book import (
    CloseBook,
)
from modules.automation.features.tax_reports.services.open_book import OpenBook
from modules.automation.features.tax_reports.services.update_book import (
    UpdateBook,
)
from modules.automation.features.tax_reports.state.book_state import BookState
from modules.automation.infrastructure.erp_session import ERPSession


class TaxBooksOrchestrator:
    def __init__(
        self,
        state: AutomationState,
        merge_spreadsheets: MergeExcelFilesService,
        open_book: OpenBook,
        update_book: UpdateBook,
        close_book: CloseBook,
        book_state: BookState,
        navigator: Navigation,
        session: ERPSession,
        save_books: SaveBooksOrchestrator,
    ):
        self.state = state
        self.session = session
        self.navigator = navigator
        self.book_state = book_state

        self.open_book = open_book
        self.update_book = update_book
        self.close_book = close_book
        self.merge_spreadsheets = merge_spreadsheets
        self.save_books = save_books

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
