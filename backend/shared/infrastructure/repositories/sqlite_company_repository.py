import logging

from core.database.base_repository import BaseRepository
from shared.domain.entities.company import Company

logger = logging.getLogger(__name__)


class CompanyRepository(BaseRepository):

    async def criar(self, company: Company) -> Company:
        company.id = await self.execute(
            """
            INSERT INTO company (codigo, nome, ativa)
            VALUES (?, ?, ?)
            """,
            (
                company.codigo,
                company.nome,
                1 if company.ativa else 0,
            ),
        )

        return company

    async def buscar_por_id(self, company_id: int) -> Company | None:
        return await self.fetch_one(
            "SELECT * FROM company WHERE id = ?",
            (company_id,),
            Company,
        )

    async def listar(self) -> list[Company]:
        return await self.fetch_all(
            "SELECT * FROM company ORDER BY nome",
            (),
            Company,
        )

    async def find_by_code(self, code: str) -> Company:
        return await self.fetch_one(
            "SELECT * FROM company WHERE codigo = ?",
            (code,),
            Company,
        )

    async def update(self, code: str, name: str):
        return await self.repo.execute(
            """
            UPDATE company
            SET nome = ?, uf = ?, cnpj = ?, ie = ?
            WHERE codigo = ?
            """,
            (
                name,
                code,
            ),
        )

    async def deletar(self, company_id: int):
        await self.execute(
            "DELETE FROM company WHERE id = ?",
            (company_id,),
        )
