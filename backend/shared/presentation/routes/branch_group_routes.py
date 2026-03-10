from fastapi import APIRouter, HTTPException, status

from core.di.container import (
    get_create_branch_group_usecase,
    get_find_branch_group_usecase,
    get_list_groups_usecase,
)
from shared.application.dto.branch_group.branch_group_response_dto import BranchGroupResponseDTO
from shared.application.dto.branch_group.create_branch_group_dto import CreateBranchGroupDTO

router = APIRouter(prefix="/branch-group", tags=["Group of branches"])


@router.post(
    "/",
    response_model=BranchGroupResponseDTO,
    status_code=status.HTTP_201_CREATED,
)
async def criar_grupo(body: CreateBranchGroupDTO):

    usecase = get_create_branch_group_usecase()

    try:
        grupo = await usecase.execute(
            codigo=body.codigo,
            nome=body.nome,
            analista=body.analista,
        )

        return BranchGroupResponseDTO.from_entity(grupo)

    except ValueError as e:
        # Validation or business rule violation
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/",
    response_model=list[BranchGroupResponseDTO],
)
async def listar_grupos():

    usecase = get_list_groups_usecase()

    grupos = await usecase.execute()

    return [BranchGroupResponseDTO.from_entity(g) for g in grupos]


@router.get(
    "/{id}",
    response_model=BranchGroupResponseDTO,
)
async def buscar_grupo(id: int):

    usecase = get_find_branch_group_usecase()

    try:
        grupo = await usecase.execute(id)

        return BranchGroupResponseDTO.from_entity(grupo)

    except LookupError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
