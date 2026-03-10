import logging
import re
from typing import Optional

from shared.domain.entities.branch import Branch
from shared.infrastructure.repositories.sqlite_branch_repository import BranchRepository
from shared.infrastructure.repositories.sqlite_company_repository import CompanyRepository

logger = logging.getLogger(__name__)


class CreateBranchUseCase:
    """
    Use case responsible for creating a Branch linked to a Company.
    """

    def __init__(
        self,
        branch_repo: BranchRepository,
        company_repo: CompanyRepository,
    ):
        # Defensive validation to avoid runtime failures if DI is misconfigured
        if branch_repo is None:
            raise ValueError("BranchRepository cannot be None")

        if company_repo is None:
            raise ValueError("CompanyRepository cannot be None")

        self.branch_repo = branch_repo
        self.company_repo = company_repo

    async def execute(
        self,
        codigo: str,
        nome: str,
        uf: str,
        cnpj: str,
        ie: str,
        company_id: int,
    ) -> Branch:
        """
        Creates a new branch for a given company.

        Args:
            codigo (str): Branch code.
            nome (str): Branch name.
            uf (str): State abbreviation.
            cnpj (str): Branch CNPJ.
            ie (str): State registration.
            company_id (int): Parent company ID.

        Returns:
            Branch: Newly created branch.

        Raises:
            ValueError: If input validation fails.
            LookupError: If company does not exist.
        """

        # ----------------------------
        # Input validation
        # ----------------------------

        if codigo is None or str(codigo).strip() == "":
            raise ValueError("Código da filial é obrigatório")

        if nome is None or nome.strip() == "":
            raise ValueError("Nome da filial é obrigatório")

        if uf is None or uf.strip() == "":
            raise ValueError("UF é obrigatória")

        if cnpj is None or cnpj.strip() == "":
            raise ValueError("CNPJ é obrigatório")

        if ie is None or ie.strip() == "":
            raise ValueError("IE é obrigatória")

        if company_id is None:
            raise ValueError("company_id é obrigatório")

        if not isinstance(company_id, int) or company_id <= 0:
            raise ValueError("company_id deve ser um inteiro positivo")

        # ----------------------------
        # Data normalization
        # ----------------------------

        # Ensure branch code is numeric and standardized
        try:
            codigo_normalizado = str(int(codigo)).zfill(3)
        except (ValueError, TypeError):
            raise ValueError("Código da filial deve ser numérico")

        nome_normalizado = nome.strip().upper()
        uf_normalizado = uf.strip().upper()

        # Remove non-numeric characters from CNPJ
        cnpj_digits = re.sub(r"\D", "", cnpj)

        if len(cnpj_digits) != 14:
            raise ValueError("CNPJ deve conter 14 dígitos")

        ie_normalizado = ie.strip()

        # ----------------------------
        # Validate company existence
        # ----------------------------

        company = await self.company_repo.buscar_por_id(company_id)

        if company is None:
            raise LookupError(f"Empresa não encontrada id={company_id}")

        # ----------------------------
        # Prevent duplicate branch codes
        # ----------------------------
        # This prevents database inconsistency if the same branch code
        # is inserted multiple times for the same company.

        existing_branch: Optional[Branch] = await self.branch_repo.fetch_one(
            "SELECT * FROM branch WHERE codigo = ? AND company_id = ?",
            (codigo_normalizado, company_id),
            Branch,
        )

        if existing_branch is not None:
            raise ValueError("Já existe uma filial com esse código para essa empresa")

        # ----------------------------
        # Create branch entity
        # ----------------------------

        branch = Branch(
            id=None,
            codigo=codigo_normalizado,
            nome=nome_normalizado,
            uf=uf_normalizado,
            cnpj=cnpj_digits,
            ie=ie_normalizado,
            company_id=company_id,
        )

        created_branch = await self.branch_repo.criar(branch)

        # Defensive check in case repository fails silently
        if created_branch is None:
            raise RuntimeError("Falha ao criar filial no repositório")

        logger.info(
            "Filial criada id=%s codigo=%s company_id=%s",
            created_branch.id,
            created_branch.codigo,
            created_branch.company_id,
        )

        return created_branch
