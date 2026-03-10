from pydantic import BaseModel


class UpdateCompanyDTO(BaseModel):
    nome: str | None = None
    ativa: bool | None = None
