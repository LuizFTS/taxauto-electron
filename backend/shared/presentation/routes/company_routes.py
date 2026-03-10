from fastapi import APIRouter, HTTPException, status

from core.di.container import (
    get_create_company_usecase,
    get_find_company_usecase,
    get_list_companies_usecase,
)
from shared.application.dto.company.company_response_dto import CompanyResponseDTO
from shared.application.dto.company.create_company_dto import CreateCompanyDTO

router = APIRouter(prefix="/companies", tags=["Companies"])


# Create
@router.post(
    "/",
    response_model=CompanyResponseDTO,
    status_code=status.HTTP_201_CREATED,
)
async def criar_empresa(body: CreateCompanyDTO):

    usecase = get_create_company_usecase()

    try:
        empresa = await usecase.execute(body)
        return CompanyResponseDTO.from_entity(empresa)

    except ValueError as e:
        # Validation or business rule violation
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# List
@router.get(
    "/",
    response_model=list[CompanyResponseDTO],
)
async def listar_empresas():

    usecase = get_list_companies_usecase()

    empresas = await usecase.execute()

    return [CompanyResponseDTO.from_entity(e) for e in empresas]


# Get by id
@router.get(
    "/{id}",
    response_model=CompanyResponseDTO,
)
async def buscar_empresa(id: int):

    usecase = get_find_company_usecase()

    try:
        empresa = await usecase.execute(id)
        return CompanyResponseDTO.from_entity(empresa)

    except LookupError as e:
        # Entity not found
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    except ValueError as e:
        # Invalid id input
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
