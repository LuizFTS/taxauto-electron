import logging
from typing import Optional

from shared.domain.entities.company import Company
from shared.infrastructure.repositories.sqlite_company_repository import CompanyRepository

logger = logging.getLogger(__name__)


class UpdateCompanyUseCase:
    """
    Use case responsible for updating company data.
    """

    def __init__(self, repo: CompanyRepository):
        # Defensive validation to ensure dependency injection is correct
        if repo is None:
            raise ValueError("CompanyRepository cannot be None")

        self.repo = repo

    async def execute(
        self,
        codigo: str,
        nome: str,
    ) -> Company:
        """
        Updates an existing company.

        Args:
            codigo (str): Company code.
            nome (str): Company name.

        Returns:
            Company: Updated company entity.

        Raises:
            ValueError: If any parameter is invalid.
            LookupError: If the company does not exist.
        """
        # ----------------------------
        # Basic input validations
        # ----------------------------

        if codigo is None or str(codigo).strip() == "":
            raise ValueError("Código da empresa é obrigatório")

        if nome is None or nome.strip() == "":
            raise ValueError("Nome da empresa é obrigatório")

        # ----------------------------
        # Data normalization
        # ----------------------------

        # Ensure company code is numeric and standardized
        try:
            codigo_normalizado = str(int(codigo)).zfill(3)
        except (ValueError, TypeError):
            raise ValueError("Código da empresa deve ser numérico")

        nome_normalizado = nome.strip().upper()

        # ----------------------------
        # Check if company exists
        # ----------------------------

        # Defensive check to avoid updating a non-existent entity
        existing_company: Optional[Company] = await self.repo.find_by_code(codigo_normalizado)

        if existing_company is None:
            raise LookupError(f"Empresa não encontrada para código={codigo_normalizado}")

        # ----------------------------
        # Perform update
        # ----------------------------

        await self.repo.update(
            nome_normalizado,
            codigo_normalizado,
        )

        # Update entity locally to reflect persisted state
        existing_company.nome = nome_normalizado

        logger.info("Empresa atualizada codigo=%s id=%s", codigo_normalizado, existing_company.id)

        return existing_company
