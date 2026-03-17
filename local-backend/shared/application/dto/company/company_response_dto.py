from pydantic import BaseModel

from shared.domain.entities.company import Company


class CompanyResponseDTO(BaseModel):
    id: int | None
    codigo: str
    nome: str
    ativa: bool

    @classmethod
    def from_entity(cls, company: Company):
        return cls(
            id=company.id,
            codigo=company.codigo,
            nome=company.nome,
            ativa=company.ativa,
        )
