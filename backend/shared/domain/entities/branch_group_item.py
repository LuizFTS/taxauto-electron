from dataclasses import dataclass


@dataclass
class BranchGroupItem:
    id: int | None
    grupo_id: int
    filial_id: int
