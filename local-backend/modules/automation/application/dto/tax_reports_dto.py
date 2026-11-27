from dataclasses import dataclass
from typing import List


@dataclass
class TaxReportsDTO:
    start_date: str
    end_date: str
    filiais: List[str]
    module: str
