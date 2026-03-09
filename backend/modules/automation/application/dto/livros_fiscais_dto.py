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
    tasks: LivrosFiscaisTasksDTO