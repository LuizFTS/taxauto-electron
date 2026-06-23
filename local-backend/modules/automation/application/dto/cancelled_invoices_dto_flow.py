from dataclasses import dataclass
from typing import List

from pydantic import BaseModel


class ValidateFileDTO(BaseModel):
    file_path: str
    file_type: str


class ValidateFileResponseDTO(BaseModel):
    is_valid: bool
    record_count: int
    message: str


@dataclass
class CancelledInvoicesFlowDTO:
    start_date: str
    end_date: str
    filiais: List[str]
    save_path: str
    login: str
    password: str

    def __post_init__(self):
        if self.filiais:
            self.filiais = sorted(self.filiais, key=int)
