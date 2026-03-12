from fastapi import APIRouter, status

from core.di.container import (
    get_add_branch_in_group_usecase,
    get_create_branch_group_usecase,
    get_find_branch_group_usecase,
    get_list_groups_usecase,
)
from shared.application.dto.branch_group.branch_group_response_dto import BranchGroupResponseDTO
from shared.application.dto.branch_group.branch_group_with_branches_dto import (
    BranchGroupWithBranchesDTO,
)
from shared.application.dto.branch_group.create_branch_group_dto import CreateBranchGroupDTO

router = APIRouter(prefix="/branch-group", tags=["Group of branches"])


@router.post(
    "/",
    response_model=BranchGroupResponseDTO,
    status_code=status.HTTP_201_CREATED,
)
async def criar_grupo(body: CreateBranchGroupDTO):

    usecase = get_create_branch_group_usecase()
    grupo = await usecase.execute(
        codigo=body.codigo,
        nome=body.nome,
        analista=body.analista,
    )

    return BranchGroupResponseDTO.from_entity(grupo)


@router.post(
    "/{group_id}/branches/{branch_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def add_branch_in_group(group_id: int, branch_id: int):

    usecase = get_add_branch_in_group_usecase()
    await usecase.execute(group_id, branch_id)


@router.get(
    "/",
    response_model=list[BranchGroupWithBranchesDTO],
)
async def listar_grupos():

    usecase = get_list_groups_usecase()
    grupos = await usecase.execute()

    return grupos


@router.get(
    "/{id}",
    response_model=BranchGroupResponseDTO,
)
async def buscar_grupo(id: int):

    usecase = get_find_branch_group_usecase()
    grupo = await usecase.execute(id)

    return BranchGroupResponseDTO.from_entity(grupo)
