import logging
from typing import Optional

from shared.domain.entities.branch import Branch
from shared.infrastructure.repositories.sqlite_branch_repository import BranchRepository

logger = logging.getLogger(__name__)


class DeleteBranchUseCase:
    """
    Use case responsible for deleting a company.
    """

    def __init__(self, repo: BranchRepository):
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
        Deletes an existing branch.

        Args:
            id (int): Branch identifier.

        Raises:
            LookupError: If the branch does not exist.
        """
        # Retrieve branch to verify existence before deletion
        existing_branch: Optional[Branch] = await self.repo.buscar_por_id(id)

        if existing_branch is None:
            raise LookupError("Filial não cadastrada com esse código")

        # Delete branch using repository
        await self.repo.delete(id)

        logger.info(
            "Filial deletada id=%s codigo=%s",
            existing_branch.id,
            existing_branch.codigo,
        )
