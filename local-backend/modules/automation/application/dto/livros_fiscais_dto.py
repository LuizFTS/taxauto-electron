from dataclasses import dataclass
from typing import List


@dataclass
class LivrosFiscaisTasksDTO:

    open_book: bool
    update_book: bool
    close_book: bool
    save_spreadsheet: bool
    save_pdf: bool


@dataclass
class LivrosFiscaisDTO:

    start_date: str
    end_date: str
    filiais: List[str]
    book_type: str
    consolidado: bool
    tasks: LivrosFiscaisTasksDTO
    save_path: str | None

    def __post_init__(self):
        if self.filiais:
            self.filiais = sorted(self.filiais, key=int)
