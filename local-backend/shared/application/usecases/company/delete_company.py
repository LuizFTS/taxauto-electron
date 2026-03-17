import logging
from typing import Optional

from shared.domain.entities.company import Company
from shared.infrastructure.repositories.sqlite_company_repository import CompanyRepository

logger = logging.getLogger(__name__)


class DeleteCompanyUseCase:
    """
    Use case responsible for deleting a company.
    """

    def __init__(self, repo: CompanyRepository):
        """
        Initialize the use case.

        Args:
            repo (CompanyRepository): Repository used to access company persistence.
        """
        # Defensive guard in case dependency injection fails
        if repo is None:
            raise ValueError("CompanyRepository cannot be None")

        self.repo = repo

    async def execute(self, id: int) -> None:
        """
        Deletes an existing company.

        Args:
            id (int): Company identifier.

        Raises:
            LookupError: If the company does not exist.
        """
        # Retrieve company to verify existence before deletion
        existing_company: Optional[Company] = await self.repo.buscar_por_id(id)

        if existing_company is None:
            raise LookupError("Empresa não cadastrada com esse código")

        # Delete company using repository
        await self.repo.delete(id)

        logger.info(
            "Empresa deletada id=%s codigo=%s",
            existing_company.id,
            existing_company.codigo,
        )
