import logging
from typing import Optional

from shared.domain.entities.branch_group import BranchGroup
from shared.infrastructure.repositories.sqlite_branch_groups_repository import BranchGroupRepository

logger = logging.getLogger(__name__)


class FindBranchGroupUseCase:
    """
    Use case responsible for retrieving a BranchGroup by its ID.
    """

    def __init__(self, repo: BranchGroupRepository):
        # Defensive validation to avoid runtime errors if dependency injection fails
        if repo is None:
            raise ValueError("BranchGroupRepository cannot be None")

        self.repo = repo

    async def execute(self, id: int) -> BranchGroup:
        """
        Retrieves a branch group by its identifier.

        Args:
            id (int): Unique identifier of the branch group.

        Returns:
            BranchGroup: The branch group entity.

        Raises:
            ValueError: If id is invalid.
            LookupError: If the group does not exist.
        """

        # ----------------------------
        # Input validation
        # ----------------------------

        if id is None:
            raise ValueError("BranchGroup id cannot be None")

        if not isinstance(id, int):
            raise TypeError("BranchGroup id must be an integer")

        if id <= 0:
            raise ValueError("BranchGroup id must be a positive integer")

        # ----------------------------
        # Fetch entity
        # ----------------------------

        group: Optional[BranchGroup] = await self.repo.buscar_por_id(id)

        # Defensive validation in case repository returns None
        if group is None:
            raise LookupError(f"Grupo de filiais não encontrado para id={id}")

        logger.info("Grupo de filiais encontrado id=%s", group.id)

        return group
