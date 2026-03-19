from dataclasses import dataclass
from typing import List


@dataclass
class MergeExcelFilesDTO:

    paths: List[str]
    output_path: str
