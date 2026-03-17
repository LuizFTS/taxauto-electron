import logging
from typing import Optional

from shared.domain.entities.company import Company
from shared.infrastructure.repositories.sqlite_company_repository import CompanyRepository

logger = logging.getLogger(__name__)


class UpdateCompanyUseCase:
    """
    Use case responsible for updating company data.
    """

    def __init__(self, repo: CompanyRepository):
        """
        Initialize the use case.

        Args:
            repo (CompanyRepository): Company persistence repository.
        """
        if repo is None:
            raise ValueError("CompanyRepository cannot be None")

        self.repo = repo

    async def execute(
        self,
        id: int,
        name: Optional[str] = None,
        ativa: Optional[bool] = None,
    ) -> None:
        """
        Updates an existing company.

        Args:
            id (int): Company identifier.
            name (Optional[str]): New company name.
            ativa (Optional[bool]): Company active status.

        Raises:
            LookupError: If the company does not exist.
        """

        # ----------------------------
        # Check if company exists
        # ----------------------------

        existing_company: Optional[Company] = await self.repo.buscar_por_id(id)

        if existing_company is None:
            raise LookupError(f"Empresa não encontrada para id={id}")

        # ----------------------------
        # Resolve final values
        # ----------------------------

        if name is not None:
            name_normalizado = name.strip().upper()

            if not name_normalizado:
                raise ValueError("Nome da empresa não pode ser vazio")
        else:
            name_normalizado = existing_company.name

        if ativa is None:
            ativa = existing_company.ativa

        # ----------------------------
        # Persist update
        # ----------------------------

        await self.repo.update(
            id,
            name_normalizado,
            ativa,
        )

        # Update in-memory entity to reflect persisted state
        existing_company.nome = name_normalizado
        existing_company.ativa = ativa

        logger.info(
            "Empresa atualizada id=%s codigo=%s",
            existing_company.id,
            existing_company.codigo,
        )
