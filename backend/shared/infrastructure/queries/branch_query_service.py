from core.database.base_query_service import BaseQueryService


class BranchQueryService(BaseQueryService):

    async def list_branches(self):

        rows = await self.fetch_all(
            """
            SELECT
                f.id,
                f.codigo,
                f.nome,
                f.uf,
                f.empresa_id,
                e.nome as empresa_nome
            FROM filial f
            JOIN empresa e ON e.id = f.empresa_id
            ORDER BY f.nome
            """
        )

        return [dict(row) for row in rows]
