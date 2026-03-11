from core.database.base_repository import BaseRepository
from shared.domain.entities.branch_group import BranchGroup


class BranchGroupRepository(BaseRepository):

    async def criar(self, grupo: BranchGroup) -> BranchGroup:
        grupo.id = await self.execute(
            """
            INSERT INTO branch_group (codigo, nome, analista)
            VALUES (?, ?, ?)
            """,
            (grupo.codigo, grupo.nome, grupo.analista),
        )

        return grupo

    async def buscar_por_id(self, branch_id: int) -> BranchGroup | None:
        return await self.fetch_one(
            "SELECT * FROM branch_group WHERE id = ?",
            (branch_id,),
            BranchGroup,
        )

    async def adicionar_filial(self, group_id: int, branch_id: int):
        await self.execute(
            """
            INSERT INTO branch_group_item (group_id, branch_id)
            VALUES (?, ?)
            """,
            (group_id, branch_id),
        )
