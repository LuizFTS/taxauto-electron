from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class StatusPeriodo(str, Enum):
    CRIADO = "CRIADO"
    IMPORTANDO = "IMPORTANDO"
    IMPORTADO = "IMPORTADO"
    PROCESSANDO = "PROCESSANDO"
    CONCLUIDO = "CONCLUIDO"
    ERRO = "ERRO"


@dataclass
class Periodo:
    ano: int
    mes: int
    status: StatusPeriodo = StatusPeriodo.CRIADO
    id: int | None = None
    criado_em: datetime | None = None
    atualizado_em: datetime | None = None

    @property
    def mes_formatado(self) -> str:
        """Retorna o mês com zero à esquerda. Ex: 3 → '03'"""
        return str(self.mes).zfill(2)

    @property
    def chave(self) -> str:
        """Identificador legível do período. Ex: '2026/03'"""
        return f"{self.ano}/{self.mes_formatado}"

    def validar(self) -> None:
        if not (2000 <= self.ano <= 2100):
            raise ValueError(f"Ano inválido: {self.ano}")
        if not (1 <= self.mes <= 12):
            raise ValueError(f"Mês inválido: {self.mes}")