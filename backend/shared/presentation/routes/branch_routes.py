from fastapi import APIRouter, HTTPException, status

from core.di.container import (
    get_create_branch_usecase,
    get_find_branch_usecase,
    get_list_all_branches_usecase,
)
from shared.application.dto.branch.branch_response_dto import BranchResponseDTO
from shared.application.dto.branch.create_branch_dto import CreateBranchDTO

router = APIRouter(prefix="/branches", tags=["Branches"])


@router.post(
    "/",
    response_model=BranchResponseDTO,
    status_code=status.HTTP_201_CREATED,
)
async def criar_filial(body: CreateBranchDTO):

    usecase = get_create_branch_usecase()

    try:
        filial = await usecase.execute(
            codigo=body.codigo,
            nome=body.nome,
            uf=body.uf,
            cnpj=body.cnpj,
            ie=body.ie,
            company_id=body.company_id,
        )

        return BranchResponseDTO.from_entity(filial)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    except LookupError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


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

    try:
        filial = await usecase.execute(id)

        return BranchResponseDTO.from_entity(filial)

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
