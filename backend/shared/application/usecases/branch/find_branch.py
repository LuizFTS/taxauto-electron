import logging
from typing import Optional

from shared.domain.entities.branch import Branch
from shared.infrastructure.repositories.sqlite_branch_repository import BranchRepository

logger = logging.getLogger(__name__)


class FindBranchUseCase:
    """
    Use case responsible for retrieving a Branch by its ID.
    """

    def __init__(self, repo: BranchRepository):
        # Defensive validation to avoid runtime errors if dependency injection fails
        if repo is None:
            raise ValueError("BranchRepository cannot be None")

        self.repo = repo

    async def execute(self, id: int) -> Branch:
        """
        Retrieves a branch by its identifier.

        Args:
            id (int): Unique identifier of the branch.

        Returns:
            Branch: The branch entity.

        Raises:
            ValueError: If the id is invalid.
            LookupError: If the branch does not exist.
        """
        # Validate input
        if id is None:
            raise ValueError("Branch id cannot be None")

        if not isinstance(id, int):
            raise TypeError("Branch id must be an integer")

        if id <= 0:
            raise ValueError("Branch id must be a positive integer")

        # Query repository
        branch: Optional[Branch] = await self.repo.buscar_por_id(id)

        # Defensive validation in case repository returns None
        if branch is None:
            raise LookupError(f"Filial não encontrada para id={id}")

        # FIX:
        # Original code used incorrect variable name and logger formatting.
        logger.info("Filial encontrada id=%s", branch.id)

        return branch
