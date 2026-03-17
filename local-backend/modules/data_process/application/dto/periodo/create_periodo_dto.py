from pydantic import BaseModel


class CreatePeriodoDTO(BaseModel):
    ano: int
    mes: int
