from core.database.base_query_service import BaseQueryService


class CompanyQueryService(BaseQueryService):

    async def list_companies_with_branches(self):
        rows = await self.fetch_all(
            """
            SELECT
                e.id   as empresa_id,
                e.codigo as empresa_codigo,
                e.nome as empresa_nome,

                f.id   as filial_id,
                f.codigo as filial_codigo,
                f.nome as filial_nome,
                f.uf   as filial_uf

            FROM empresa e
            LEFT JOIN filial f ON f.empresa_id = e.id
            ORDER BY e.nome, f.nome
            """
        )

        companies = {}

        for row in rows:
            eid = row["empresa_id"]

            if eid not in companies:
                companies[eid] = {
                    "id": eid,
                    "numero": row["empresa_codigo"],
                    "nome": row["empresa_nome"],
                    "filiais": [],
                }

            if row["filial_id"]:
                companies[eid]["filiais"].append(
                    {
                        "id": row["filial_id"],
                        "numero": row["filial_codigo"],
                        "nome": row["filial_nome"],
                        "uf": row["filial_uf"],
                    }
                )

        return list(companies.values())
