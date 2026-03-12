import logging
from typing import Optional

from shared.domain.entities.branch import Branch
from shared.domain.entities.branch_group import BranchGroup
from shared.infrastructure.repositories.sqlite_branch_groups_repository import BranchGroupRepository
from shared.infrastructure.repositories.sqlite_branch_repository import BranchRepository

logger = logging.getLogger(__name__)


class AddBranchInGroupUseCase:
    """
    Use case responsible for associating a Branch with a BranchGroup.
    """

    def __init__(
        self,
        group_repo: BranchGroupRepository,
        branch_repo: BranchRepository,
    ):
        # Defensive validation to ensure dependency injection worked
        if group_repo is None:
            raise ValueError("BranchGroupRepository cannot be None")

        if branch_repo is None:
            raise ValueError("BranchRepository cannot be None")

        self.group_repo = group_repo
        self.branch_repo = branch_repo

    async def execute(self, group_id: int, branch_id: int) -> None:
        """
        Adds a branch to a branch group.

        Args:
            group_id (int): Identifier of the group.
            branch_id (int): Identifier of the branch.

        Raises:
            ValueError: If inputs are invalid.
            LookupError: If the branch or group does not exist.
        """

        # ----------------------------
        # Input validation
        # ----------------------------

        if group_id is None:
            raise ValueError("group_id cannot be None")

        if branch_id is None:
            raise ValueError("branch_id cannot be None")

        if not isinstance(group_id, int) or group_id <= 0:
            raise ValueError("group_id must be a positive integer")

        if not isinstance(branch_id, int) or branch_id <= 0:
            raise ValueError("branch_id must be a positive integer")

        # ----------------------------
        # Validate branch existence
        # ----------------------------

        branch: Optional[Branch] = await self.branch_repo.buscar_por_id(branch_id)

        if branch is None:
            raise LookupError(f"Filial não encontrada id={branch_id}")

        # ----------------------------
        # Validate group existence
        # ----------------------------

        group: Optional[BranchGroup] = await self.group_repo.buscar_por_id(group_id)

        if group is None:
            raise LookupError(f"Grupo de filiais não encontrado id={group_id}")

        # ----------------------------
        # Prevent duplicate association
        # ----------------------------
        # Avoid inserting the same branch into the same group multiple times.

        exists = await self.group_repo.fetch_one(
            """
        SELECT 1
        FROM branch_group_item
        WHERE group_id = ? AND branch_id = ?
        """,
            (group_id, branch_id),
            None,
        )

        if exists:
            raise ValueError("Filial já está associada a este grupo")

        # ----------------------------
        # Create association
        # ----------------------------

        await self.group_repo.adicionar_filial(group_id, branch_id)

        logger.info(
            "Filial %s adicionada ao grupo %s",
            branch_id,
            group_id,
        )
