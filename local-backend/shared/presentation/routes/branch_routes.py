from fastapi import APIRouter, status

from core.di.container import (
    get_create_branch_usecase,
    get_delete_branch_usecase,
    get_find_branch_usecase,
    get_list_all_branches_usecase,
    get_update_branch_usecase,
)
from shared.application.dto.branch.branch_response_dto import BranchResponseDTO
from shared.application.dto.branch.create_branch_dto import CreateBranchDTO
from shared.application.dto.branch.update_branch_dto import UpdateBranchDTO

router = APIRouter(prefix="/branches", tags=["Branches"])


@router.post(
    "/",
    response_model=BranchResponseDTO,
    status_code=status.HTTP_201_CREATED,
)
async def criar_filial(body: CreateBranchDTO):

    usecase = get_create_branch_usecase()
    filial = await usecase.execute(
        codigo=body.codigo,
        nome=body.nome,
        uf=body.uf,
        cnpj=body.cnpj,
        ie=body.ie,
        company_id=body.company_id,
    )

    return BranchResponseDTO.from_entity(filial)


@router.get(
    "/",
    response_model=list[BranchResponseDTO],
)
async def listar_filiais():

    usecase = get_list_all_branches_usecase()
    filiais = await usecase.execute()

    return [BranchResponseDTO.from_entity(f) for f in filiais]


@router.get(
    "/{id}",
    response_model=BranchResponseDTO,
)
async def buscar_filial(id: int):

    usecase = get_find_branch_usecase()
    filial = await usecase.execute(id)

    return BranchResponseDTO.from_entity(filial)


# Delete by id
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_branch(id: int):

    usecase = get_delete_branch_usecase()
    await usecase.execute(id)


# Update by id
@router.patch("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_branch(id: int, body: UpdateBranchDTO):

    usecase = get_update_branch_usecase()
    await usecase.execute(
        id=id,
        name=body.name,
        uf=body.uf,
        cnpj=body.cnpj,
        ie=body.ie,
        company_id=body.company_id,
        ativa=body.ativa,
    )
