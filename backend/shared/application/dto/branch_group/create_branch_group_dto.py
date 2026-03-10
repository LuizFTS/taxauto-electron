from pydantic import BaseModel


class CreateBranchGroupDTO(BaseModel):
    codigo: str
    nome: str
    analista: str
