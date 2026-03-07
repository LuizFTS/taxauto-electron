import logging
from datetime import datetime

from core.database.connection import session
from modules.data_process.domain.entities.periodo import Periodo, StatusPeriodo

logger = logging.getLogger(__name__)


class PeriodoRepository:

    async def criar(self, periodo: Periodo) -> Periodo:
        async with session() as conn:
            cursor = await conn.execute(
                """
                INSERT INTO periodo (ano, mes, status)
                VALUES (?, ?, ?)
                """,
                (periodo.ano, periodo.mes, periodo.status.value),
            )
            await conn.commit()
            periodo.id = cursor.lastrowid
            logger.info("Período criado: id=%s chave=%s", periodo.id, periodo.chave)
            return periodo

    async def buscar_por_id(self, id: int) -> Periodo | None:
        async with session() as conn:
            async with conn.execute("SELECT * FROM periodo WHERE id = ?", (id,)) as cursor:
                row = await cursor.fetchone()
                return self._row_to_entity(row) if row else None

    async def buscar_por_ano_mes(self, ano: int, mes: int) -> Periodo | None:
        async with session() as conn:
            async with conn.execute(
                "SELECT * FROM periodo WHERE ano = ? AND mes = ?", (ano, mes)
            ) as cursor:
                row = await cursor.fetchone()
                return self._row_to_entity(row) if row else None

    async def listar(self) -> list[Periodo]:
        async with session() as conn:
            async with conn.execute("SELECT * FROM periodo ORDER BY ano DESC, mes DESC") as cursor:
                rows = await cursor.fetchall()
                return [self._row_to_entity(r) for r in rows]

    async def atualizar_status(self, id: int, status: StatusPeriodo) -> None:
        async with session() as conn:
            await conn.execute(
                """
                UPDATE periodo
                SET status = ?, atualizado_em = datetime('now', 'localtime')
                WHERE id = ?
                """,
                (status.value, id),
            )
            await conn.commit()
            logger.info("Status do período %s atualizado para %s", id, status.value)

    def _row_to_entity(self, row) -> Periodo:
        return Periodo(
            id=row["id"],
            ano=row["ano"],
            mes=row["mes"],
            status=StatusPeriodo(row["status"]),
            criado_em=datetime.fromisoformat(row["criado_em"]),
            atualizado_em=datetime.fromisoformat(row["atualizado_em"]),
        )
