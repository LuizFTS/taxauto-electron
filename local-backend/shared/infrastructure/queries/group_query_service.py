from core.database.base_query_service import BaseQueryService


class GroupQueryService(BaseQueryService):

    async def list_groups_with_branches(self):

        rows = await self.fetch_all(
            """
            SELECT
                bg.id as grupo_id,
                bg.nome as grupo_nome,
                bg.analista as analista_grupo,
                b.id as branch_id,
                b.codigo as branch_code,
                b.nome as branch_name,
                b.uf as branch_uf
            FROM branch_group bg
            LEFT JOIN branch_group_item bgi
                ON bgi.group_id = bg.id
            LEFT JOIN branch b
                ON b.id = bgi.branch_id
            ORDER BY bg.nome, b.nome
            """
        )

        groups = {}

        for row in rows:

            gid = row["grupo_id"]

            if gid not in groups:
                groups[gid] = {
                    "id": gid,
                    "name": row["grupo_nome"],
                    "analyst": row["analista_grupo"],
                    "branches": [],
                }

            if row["branch_id"]:
                groups[gid]["branches"].append(
                    {
                        "id": row["branch_id"],
                        "codigo": row["branch_code"],
                        "name": row["branch_name"],
                        "uf": row["branch_uf"],
                    }
                )

        return list(groups.values())
