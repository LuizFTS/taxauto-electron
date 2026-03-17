import logging
from typing import Optional

from shared.application.dto.company.create_company_dto import CreateCompanyDTO
from shared.domain.entities.company import Company
from shared.infrastructure.repositories.sqlite_company_repository import CompanyRepository

logger = logging.getLogger(__name__)


class CreateCompanyUseCase:
    """
    Use case responsible for creating a new Company entity.

    This class validates the input DTO, checks for existing companies
    with the same code, normalizes the data, and persists the entity
    using the repository.
    """

    def __init__(self, repo: CompanyRepository):
        # Defensive check to avoid runtime errors if dependency injection fails
        if repo is None:
            raise ValueError("CompanyRepository cannot be None")
        self.repo = repo

    async def execute(self, dto: CreateCompanyDTO) -> Company:
        """
        Creates a new company.

        Args:
            dto (CreateCompanyDTO): Data required to create a company.

        Returns:
            Company: The newly created company entity.

        Raises:
            ValueError: If input data is invalid or the company already exists.
        """
        # Validate DTO presence
        if dto is None:
            raise ValueError("CreateCompanyDTO cannot be None")

        # Validate company code
        if dto.codigo is None or str(dto.codigo).strip() == "":
            raise ValueError("Código da empresa é obrigatório")

        # Validate company name
        if dto.nome is None or str(dto.nome).strip() == "":
            raise ValueError("Nome da empresa é obrigatório")

        # Ensure codigo is numeric before casting to int
        try:
            codigo_normalizado = str(int(dto.codigo)).zfill(3)
        except (ValueError, TypeError):
            raise ValueError("Código da empresa deve ser numérico")

        # Normalize name to uppercase to keep database consistency
        nome_normalizado = dto.nome.strip().upper()

        # Check if a company with the same code already exists
        existing_company: Optional[Company] = await self.repo.find_by_code(codigo_normalizado)

        # raise an error if the company ALREADY exists.
        if existing_company is not None:
            raise ValueError("Empresa com esse código já cadastrada")

        # Create the domain entity
        new_company = Company(
            id=None,
            codigo=codigo_normalizado,
            nome=nome_normalizado,
            ativa=True,
        )

        # Persist entity using repository
        created_company = await self.repo.criar(new_company)

        # Defensive validation in case repository returns an invalid result
        if created_company is None:
            raise RuntimeError("Falha ao criar empresa no repositório")

        logger.info("Empresa criada id=%s codigo=%s", created_company.id, created_company.codigo)

        return created_company
