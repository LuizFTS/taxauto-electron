import logging
from dataclasses import dataclass

from modules.data_process.domain.entities.periodo import Periodo
from modules.data_process.infrastructure.repositories.sqlite_period_repository import (
    PeriodoRepository,
)
from shared.infrastructure.filesystem.workspace_manager import WorkspaceManager

logger = logging.getLogger(__name__)


@dataclass
class CreatePeriodInput:
    ano: int
    mes: int


@dataclass
class CreatePeriodOutput:
    periodo: Periodo
    workspace_paths: dict
    appdata_paths: dict
    ja_existia: bool


class CreatePeriodUseCase:
    """
    Orquestra a criação de um novo período fiscal.

    Responsabilidades:
    - Validar os dados do período
    - Verificar se o período já existe
    - Persistir no banco de dados
    - Criar a estrutura de diretórios (workspace + appdata)
    """

    def __init__(
        self,
        repository: PeriodoRepository,
        workspace: WorkspaceManager,
    ) -> None:
        self._repository = repository
        self._workspace = workspace

    async def executar(self, input_data: CreatePeriodInput) -> CreatePeriodOutput:
        periodo = Periodo(ano=input_data.ano, mes=input_data.mes)
        periodo.validar()

        # Verifica se o período já existe no banco
        existente = await self._repository.buscar_por_ano_mes(input_data.ano, input_data.mes)
        if existente:
            logger.info("Período %s já existe (id=%s)", existente.chave, existente.id)

            # Garante que os diretórios existam mesmo que o período já estivesse no banco
            workspace_paths = self._workspace.criar_estrutura_periodo(existente)
            appdata_paths = self._workspace.criar_estrutura_appdata(existente)

            return CreatePeriodOutput(
                periodo=existente,
                workspace_paths={k: str(v) for k, v in workspace_paths.items()},
                appdata_paths={k: str(v) for k, v in appdata_paths.items()},
                ja_existia=True,
            )

        # Persiste o novo período
        novo_periodo = await self._repository.criar(periodo)

        # Cria estrutura de pastas
        workspace_paths = self._workspace.criar_estrutura_periodo(novo_periodo)
        appdata_paths = self._workspace.criar_estrutura_appdata(novo_periodo)

        logger.info("Período %s criado com sucesso.", novo_periodo.chave)

        return CreatePeriodOutput(
            periodo=novo_periodo,
            workspace_paths={k: str(v) for k, v in workspace_paths.items()},
            appdata_paths={k: str(v) for k, v in appdata_paths.items()},
            ja_existia=False,
        )