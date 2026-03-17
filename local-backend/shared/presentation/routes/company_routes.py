from fastapi import APIRouter, status

from core.di.container import (
    get_create_company_usecase,
    get_delete_company_usecase,
    get_find_company_usecase,
    get_list_companies_usecase,
    get_update_company_usecase,
)
from shared.application.dto.company.company_response_dto import CompanyResponseDTO
from shared.application.dto.company.create_company_dto import CreateCompanyDTO
from shared.application.dto.company.update_company_dto import UpdateCompanyDTO

router = APIRouter(prefix="/companies", tags=["Companies"])


# Create
@router.post(
    "/",
    response_model=CompanyResponseDTO,
    status_code=status.HTTP_201_CREATED,
)
async def criar_empresa(body: CreateCompanyDTO):

    usecase = get_create_company_usecase()
    empresa = await usecase.execute(body)

    return CompanyResponseDTO.from_entity(empresa)


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
    empresa = await usecase.execute(id)

    return CompanyResponseDTO.from_entity(empresa)


# Delete by id
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(id: int):

    usecase = get_delete_company_usecase()
    await usecase.execute(id)


# Update by id
@router.patch("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_company(id: int, body: UpdateCompanyDTO):

    usecase = get_update_company_usecase()
    await usecase.execute(id=id, name=body.name, ativa=body.ativa)
