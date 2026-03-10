from core.database.base_query_service import BaseQueryService


class GroupQueryService(BaseQueryService):

    async def list_groups_with_branches(self):

        rows = await self.fetch_all(
            """
            SELECT
                g.id as grupo_id,
                g.nome as grupo_nome,

                f.id as filial_id,
                f.codigo as filial_codigo,
                f.nome as filial_nome,
                f.uf as filial_uf

            FROM grupo_filiais g
            LEFT JOIN grupo_filial_item gfi
                ON gfi.grupo_id = g.id

            LEFT JOIN filial f
                ON f.id = gfi.filial_id

            ORDER BY g.nome, f.nome
            """
        )

        groups = {}

        for row in rows:

            gid = row["grupo_id"]

            if gid not in groups:
                groups[gid] = {
                    "id": gid,
                    "name": row["grupo_nome"],
                    "branches": [],
                }

            if row["filial_id"]:
                groups[gid]["branches"].append(
                    {
                        "id": row["filial_id"],
                        "numero": row["filial_codigo"],
                        "nome": row["filial_nome"],
                        "uf": row["filial_uf"],
                    }
                )

        return list(groups.values())
