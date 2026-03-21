from dataclasses import dataclass
from typing import List


@dataclass
class CancelledInvoicesDTO:

    start_date: str
    end_date: str
    filiais: List[str]
    save_path: str | None
    login: str
    password: str

    def __post_init__(self):
        if self.filiais:
            self.filiais = sorted(self.filiais, key=int)
