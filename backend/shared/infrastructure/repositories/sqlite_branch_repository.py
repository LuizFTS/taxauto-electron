from core.database.base_repository import BaseRepository
from shared.domain.entities.branch import Branch


class BranchRepository(BaseRepository):

    async def criar(self, branch: Branch) -> Branch:
        branch.id = await self.execute(
            """
            INSERT INTO branch
            (codigo, nome, uf, cnpj, ie, company_id, ativa)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                branch.codigo,
                branch.nome,
                branch.uf,
                branch.cnpj,
                branch.ie,
                branch.company_id,
                1 if branch.ativa else 0,
            ),
        )

        return branch

    async def listar_por_empresa(self, company_id: int):
        return await self.fetch_all(
            "SELECT * FROM branch WHERE company_id = ?",
            (company_id,),
            Branch,
        )

    async def buscar_por_id(self, branch_id: int) -> Branch | None:
        return await self.fetch_one(
            "SELECT * FROM branch WHERE id = ?",
            (branch_id,),
            Branch,
        )

    async def list_all(self):
        return await self.fetch_all("SELECT * FROM branch", params=(), entity=Branch)
