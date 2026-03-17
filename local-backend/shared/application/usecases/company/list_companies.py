import logging
from typing import List

from shared.domain.entities.company import Company
from shared.infrastructure.repositories.sqlite_company_repository import CompanyRepository

logger = logging.getLogger(__name__)


class ListCompaniesUseCase:
    """
    Use case responsible for retrieving all companies from the repository.
    """

    def __init__(self, repo: CompanyRepository):
        # Defensive validation to ensure dependency injection worked correctly.
        # Prevents attribute errors later when calling repository methods.
        if repo is None:
            raise ValueError("CompanyRepository cannot be None")

        self.repo = repo

    async def execute(self) -> List[Company]:
        """
        Returns a list of all companies.

        Returns:
            List[Company]: List containing Company entities.

        Raises:
            RuntimeError: If the repository returns an invalid result.
        """

        # Fetch companies from repository
        companies = await self.repo.listar()

        # Defensive validation:
        # Repository implementations should return a list.
        # If None is returned, it indicates an implementation error.
        if companies is None:
            raise RuntimeError("Repository returned None when listing companies")

        # Ensure the returned value is a list to avoid unexpected runtime behavior.
        if not isinstance(companies, list):
            raise TypeError("Repository must return a list of Company objects")

        # Optional defensive check to ensure list elements are valid entities.
        for company in companies:
            if not isinstance(company, Company):
                raise TypeError("Repository returned an invalid Company object")

        logger.info("Empresas listadas total=%s", len(companies))

        return companies
