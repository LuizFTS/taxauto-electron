from dataclasses import dataclass
from datetime import datetime


@dataclass
class Company:
    id: int | None
    codigo: str
    nome: str
    ativa: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None
