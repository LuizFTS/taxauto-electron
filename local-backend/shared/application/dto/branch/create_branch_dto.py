from pydantic import BaseModel


class CreateBranchDTO(BaseModel):
    codigo: str
    nome: str
    uf: str
    cnpj: str
    ie: str | None
    company_id: int
