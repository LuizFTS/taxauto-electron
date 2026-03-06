from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, field_validator
from domain.models.periodo import StatusPeriodo
from application.usecases.create_period import CreatePeriodInput, CreatePeriodUseCase
from infrastructure.database.repositories.periodo_repository import PeriodoRepository
from infrastructure.filesystem.workspace_manager import WorkspaceManager

router = APIRouter(prefix="/periodos", tags=["Períodos"])

# ---------------------------------------------------------------------------
# Schemas de request / response
# ---------------------------------------------------------------------------

class CriarPeriodoRequest(BaseModel):
    ano: int
    mes: int

    @field_validator("ano")
    @classmethod
    def validar_ano(cls, v: int) -> int:
        if not (2000 <= v <= 2100):
            raise ValueError("Ano deve estar entre 2000 e 2100")
        return v

    @field_validator("mes")
    @classmethod
    def validar_mes(cls, v: int) -> int:
        if not (1 <= v <= 12):
            raise ValueError("Mês deve estar entre 1 e 12")
        return v


class PeriodoResponse(BaseModel):
    id: int | None
    ano: int
    mes: int
    chave: str
    status: StatusPeriodo
    criado_em: str | None
    atualizado_em: str | None


class CriarPeriodoResponse(BaseModel):
    periodo: PeriodoResponse
    workspace_paths: dict[str, str]
    appdata_paths: dict[str, str]
    ja_existia: bool
    mensagem: str


# ---------------------------------------------------------------------------
# Dependency factories (simples, sem DI container por ora)
# ---------------------------------------------------------------------------

def get_usecase() -> CreatePeriodUseCase:
    return CreatePeriodUseCase(
        repository=PeriodoRepository(),
        workspace=WorkspaceManager(),
    )


def get_repository() -> PeriodoRepository:
    return PeriodoRepository()


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post(
    "/",
    response_model=CriarPeriodoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo período fiscal",
)
async def criar_periodo(body: CriarPeriodoRequest):
    usecase = get_usecase()
    result = await usecase.executar(CreatePeriodInput(ano=body.ano, mes=body.mes))

    periodo = result.periodo
    return CriarPeriodoResponse(
        periodo=PeriodoResponse(
            id=periodo.id,
            ano=periodo.ano,
            mes=periodo.mes,
            chave=periodo.chave,
            status=periodo.status,
            criado_em=periodo.criado_em.isoformat() if periodo.criado_em else None,
            atualizado_em=periodo.atualizado_em.isoformat() if periodo.atualizado_em else None,
        ),
        workspace_paths=result.workspace_paths,
        appdata_paths=result.appdata_paths,
        ja_existia=result.ja_existia,
        mensagem=(
            f"Período {periodo.chave} já existia e foi retornado."
            if result.ja_existia
            else f"Período {periodo.chave} criado com sucesso."
        ),
    )


@router.get(
    "/",
    response_model=list[PeriodoResponse],
    summary="Lista todos os períodos fiscais",
)
async def listar_periodos():
    repo = get_repository()
    periodos = await repo.listar()
    return [
        PeriodoResponse(
            id=p.id,
            ano=p.ano,
            mes=p.mes,
            chave=p.chave,
            status=p.status,
            criado_em=p.criado_em.isoformat() if p.criado_em else None,
            atualizado_em=p.atualizado_em.isoformat() if p.atualizado_em else None,
        )
        for p in periodos
    ]


@router.get(
    "/{id}",
    response_model=PeriodoResponse,
    summary="Busca um período por ID",
)
async def buscar_periodo(id: int):
    repo = get_repository()
    periodo = await repo.buscar_por_id(id)
    if not periodo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Período com id={id} não encontrado.",
        )
    return PeriodoResponse(
        id=periodo.id,
        ano=periodo.ano,
        mes=periodo.mes,
        chave=periodo.chave,
        status=periodo.status,
        criado_em=periodo.criado_em.isoformat() if periodo.criado_em else None,
        atualizado_em=periodo.atualizado_em.isoformat() if periodo.atualizado_em else None,
    )