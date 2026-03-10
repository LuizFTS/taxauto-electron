import logging
from typing import Optional

from shared.domain.entities.branch_group import BranchGroup
from shared.infrastructure.repositories.sqlite_branch_groups_repository import (
    BranchGroupRepository,
)

logger = logging.getLogger(__name__)


class CreateBranchGroupUseCase:
    """
    Use case responsible for creating a group of branches assigned to an analyst.
    """

    def __init__(self, repo: BranchGroupRepository):
        # Defensive validation to prevent runtime errors if dependency injection fails
        if repo is None:
            raise ValueError("BranchGroupRepository cannot be None")

        self.repo = repo

    async def execute(
        self,
        codigo: str,
        nome: str,
        analista: str,
    ) -> BranchGroup:
        """
        Creates a new BranchGroup.

        Args:
            codigo (str): Group code.
            nome (str): Group name.
            analista (str): Analyst responsible for the group.

        Returns:
            BranchGroup: Newly created group.

        Raises:
            ValueError: If input validation fails.
        """
        # ----------------------------
        # Input validation
        # ----------------------------

        if codigo is None or str(codigo).strip() == "":
            raise ValueError("Código do grupo é obrigatório")

        if nome is None or nome.strip() == "":
            raise ValueError("Nome do grupo é obrigatório")

        if analista is None or analista.strip() == "":
            raise ValueError("Analista é obrigatório")

        # ----------------------------
        # Data normalization
        # ----------------------------

        # Ensure group code is numeric and standardized
        try:
            codigo_normalizado = str(int(codigo)).zfill(3)
        except (ValueError, TypeError):
            raise ValueError("Código do grupo deve ser numérico")

        nome_normalizado = nome.strip().upper()
        analista_normalizado = analista.strip()

        # ----------------------------
        # Prevent duplicate group code
        # ----------------------------
        # Avoid creating multiple groups with the same code.

        existing_group: Optional[BranchGroup] = await self.repo.fetch_one(
            "SELECT * FROM branch_group WHERE codigo = ?",
            (codigo_normalizado,),
            BranchGroup,
        )

        if existing_group is not None:
            raise ValueError("Já existe um grupo com esse código")

        # ----------------------------
        # Create entity
        # ----------------------------

        grupo = BranchGroup(
            id=None,
            codigo=codigo_normalizado,
            nome=nome_normalizado,
            analista=analista_normalizado,
        )

        created_group = await self.repo.criar(grupo)

        # Defensive validation in case repository fails silently
        if created_group is None:
            raise RuntimeError("Falha ao criar grupo no repositório")

        logger.info(
            "Grupo criado id=%s codigo=%s analista=%s",
            created_group.id,
            created_group.codigo,
            created_group.analista,
        )

        return created_group
