from pydantic import BaseModel


class UpdateBranchDTO(BaseModel):
    name: str | None
    uf: str | None
    cnpj: str | None
    ie: str | None
    company_id: int | None
    ativa: bool | None
