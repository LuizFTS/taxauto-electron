from dataclasses import dataclass
from typing import List


@dataclass
class TaxAssessmentReportDTO:
    date: str
    filiais: List[str]
    save_path: str | None

    def __post_init__(self):
        if self.filiais:
            self.filiais = sorted(self.filiais, key=int)
