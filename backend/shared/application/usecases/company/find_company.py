import logging
from typing import Optional

from shared.domain.entities.company import Company
from shared.infrastructure.repositories.sqlite_company_repository import CompanyRepository

logger = logging.getLogger(__name__)


class FindCompanyUseCase:
    """
    Use case responsible for retrieving a Company by its ID.
    """

    def __init__(self, repo: CompanyRepository):
        # Defensive validation to avoid runtime issues if dependency injection fails
        if repo is None:
            raise ValueError("CompanyRepository cannot be None")
        self.repo = repo

    async def execute(self, id: int) -> Company:
        """
        Retrieves a company by its identifier.

        Args:
            id (int): Unique identifier of the company.

        Returns:
            Company: The company entity.

        Raises:
            ValueError: If the id is invalid.
            LookupError: If no company is found with the given id.
        """

        # Validate input type and value
        if id is None:
            raise ValueError("Company id cannot be None")

        if not isinstance(id, int):
            raise TypeError("Company id must be an integer")

        if id <= 0:
            raise ValueError("Company id must be a positive integer")

        # Query repository
        company: Optional[Company] = await self.repo.buscar_por_id(id)

        # Defensive validation: repository may return None if entity does not exist
        if company is None:
            raise LookupError(f"Empresa não encontrada para id={id}")

        logger.info("Empresa encontrada id=%s", company.id)

        return company
