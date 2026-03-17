from pydantic import BaseModel

from modules.data_process.domain.entities.periodo import Periodo, StatusPeriodo


class PeriodoResponseDTO(BaseModel):
    id: int | None
    ano: int
    mes: int
    chave: str
    status: StatusPeriodo
    criado_em: str | None
    atualizado_em: str | None

    @classmethod
    def from_entity(cls, periodo: Periodo):
        return cls(
            id=periodo.id,
            ano=periodo.ano,
            mes=periodo.mes,
            chave=periodo.chave,
            status=periodo.status,
            criado_em=periodo.criado_em.isoformat() if periodo.criado_em else None,
            atualizado_em=periodo.atualizado_em.isoformat() if periodo.atualizado_em else None,
        )
