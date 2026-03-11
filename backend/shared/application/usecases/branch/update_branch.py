import logging
from typing import Optional

from shared.domain.entities.branch import Branch
from shared.infrastructure.repositories.sqlite_branch_repository import BranchRepository

logger = logging.getLogger(__name__)


class UpdateBranchUseCase:
    """
    Use case responsible for updating branch data.
    """

    def __init__(self, repo: BranchRepository):
        """
        Initialize the use case.

        Args:
            repo (branchRepository): branch persistence repository.
        """
        if repo is None:
            raise ValueError("branchRepository cannot be None")

        self.repo = repo

    async def execute(
        self,
        id: int,
        name: Optional[str] = None,
        uf: Optional[str] = None,
        cnpj: Optional[str] = None,
        ie: Optional[str] = None,
        company_id: Optional[int] = None,
        ativa: Optional[bool] = None,
    ) -> None:
        """
        Updates an existing branch.

        Args:
            id (int): branch identifier.
            nome (Optional[str]): New branch name.
            ativa (Optional[bool]): branch active status.

        Raises:
            LookupError: If the branch does not exist.
        """

        # ----------------------------
        # Check if branch exists
        # ----------------------------

        existing_branch: Optional[Branch] = await self.repo.buscar_por_id(id)

        if existing_branch is None:
            raise LookupError(f"Empresa não encontrada para id={id}")

        # ----------------------------
        # Resolve final values
        # ----------------------------

        if name is not None:
            name_normalizado = name.strip().upper()

            if not name_normalizado:
                raise ValueError("Nome da empresa não pode ser vazio")
        else:
            name_normalizado = existing_branch.name

        if ativa is None:
            ativa = existing_branch.ativa

        # ----------------------------
        # Persist update
        # ----------------------------

        await self.repo.update(
            id,
            name,
            uf,
            cnpj,
            ie,
            company_id,
            ativa,
        )

        # Update in-memory entity to reflect persisted state
        existing_branch.name = name_normalizado
        existing_branch.ativa = ativa

        logger.info(
            "Empresa atualizada id=%s codigo=%s",
            existing_branch.id,
            existing_branch.codigo,
        )
