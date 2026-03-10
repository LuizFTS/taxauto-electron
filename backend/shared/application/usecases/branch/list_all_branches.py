import logging
from typing import List

from shared.domain.entities.branch import Branch
from shared.infrastructure.repositories.sqlite_branch_repository import BranchRepository
from shared.infrastructure.repositories.sqlite_company_repository import CompanyRepository

logger = logging.getLogger(__name__)


class ListAllBranchesUseCase:
    """
    Use case responsible for retrieving all branches.
    """

    def __init__(
        self,
        branch_repo: BranchRepository,
        company_repo: CompanyRepository,
    ):
        # Defensive validation to prevent runtime errors if dependency injection fails
        if branch_repo is None:
            raise ValueError("BranchRepository cannot be None")

        if company_repo is None:
            raise ValueError("CompanyRepository cannot be None")

        self.branch_repo = branch_repo
        self.company_repo = company_repo

    async def execute(self) -> List[Branch]:
        """
        Returns a list of all branches.

        Returns:
            List[Branch]: Collection of Branch entities.

        Raises:
            RuntimeError: If the repository returns an invalid result.
        """
        branches = await self.branch_repo.list_all()

        # Defensive validation: repository implementations should return a list
        if branches is None:
            raise RuntimeError("Repository returned None when listing branches")

        if not isinstance(branches, list):
            raise TypeError("Repository must return a list of Branch objects")

        # Ensure all items are valid Branch entities
        for branch in branches:
            if not isinstance(branch, Branch):
                raise TypeError("Repository returned an invalid Branch object")

        logger.info("Filiais listadas total=%s", len(branches))

        return branches
