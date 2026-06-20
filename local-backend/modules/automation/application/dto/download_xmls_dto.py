from dataclasses import dataclass
from typing import List


@dataclass
class DownloadXmlsDTO:

    start_date: str
    end_date: str
    filiais: List[str]
    save_path: str
    login: str
    password: str
    tipo_documento: int
    tipo_operacao: int

    def __post_init__(self):
        if self.filiais:
            self.filiais = sorted(self.filiais, key=int)
