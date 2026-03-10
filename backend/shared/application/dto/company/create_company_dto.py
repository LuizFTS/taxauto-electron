from pydantic import BaseModel


class CreateCompanyDTO(BaseModel):
    codigo: str
    nome: str
