from pydantic import BaseModel

from shared.domain.entities.branch import Branch


class BranchResponseDTO(BaseModel):
    id: int | None
    codigo: str
    nome: str
    uf: str
    cnpj: str
    ie: str | None
    company_id: int

    @classmethod
    def from_entity(cls, branch: Branch):
        return cls(
            id=branch.id,
            codigo=branch.codigo,
            nome=branch.nome,
            uf=branch.uf,
            cnpj=branch.cnpj,
            ie=branch.ie,
            company_id=branch.company_id,
        )
