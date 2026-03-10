from dataclasses import dataclass
from datetime import datetime


@dataclass
class Branch:
    id: int | None
    codigo: str
    nome: str
    uf: str
    cnpj: str
    ie: str
    company_id: int
    ativa: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None
