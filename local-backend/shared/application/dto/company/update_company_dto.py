from pydantic import BaseModel


class UpdateCompanyDTO(BaseModel):
    name: str | None = None
    ativa: bool | None = None
