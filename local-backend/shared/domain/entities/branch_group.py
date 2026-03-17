from dataclasses import dataclass
from datetime import datetime


@dataclass
class BranchGroup:
    id: int | None
    codigo: str
    nome: str
    analista: str | None = None
    ativo: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None
