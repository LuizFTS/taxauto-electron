import logging
from pathlib import Path

from core.config.settings import settings
from modules.data_process.domain.entities.periodo import Periodo

logger = logging.getLogger(__name__)


class WorkspaceManager:
    """
    Gerencia a estrutura de diretórios no Documents do usuário.
    Responsável por criar e validar os caminhos do workspace.
    """

    def criar_estrutura_periodo(self, periodo: Periodo) -> dict[str, Path]:
        """
        Cria a estrutura de pastas para um período fiscal.

        Documents/Apuracao_ICMS/{ano}/{mes}/
            input/
                LIVRO_ENTRADA/
                LIVRO_SAIDA/
                ... (demais tipos)
            resultados/
        """
        raiz = self._raiz_periodo(periodo)

        pastas_criadas: dict[str, Path] = {}

        # Subpastas de input
        for nome_pasta in settings.INPUT_FOLDERS:
            caminho = raiz / "input" / nome_pasta
            caminho.mkdir(parents=True, exist_ok=True)
            pastas_criadas[nome_pasta] = caminho

        # Pasta de resultados
        resultados = raiz / "resultados"
        resultados.mkdir(parents=True, exist_ok=True)
        pastas_criadas["resultados"] = resultados

        logger.info("Workspace criado: %s", raiz)
        return pastas_criadas

    def criar_estrutura_appdata(self, periodo: Periodo) -> dict[str, Path]:
        """
        Cria a estrutura interna de armazenamento da aplicação (AppData).

        AppData/icms_apurador/data/{ano}/{mes}/
            raw/
            processed/
            output/
        """
        raiz = self._raiz_appdata(periodo)

        pastas = {
            "raw":       raiz / "raw",
            "processed": raiz / "processed",
            "output":    raiz / "output",
        }

        for caminho in pastas.values():
            caminho.mkdir(parents=True, exist_ok=True)

        logger.info("AppData do período criado: %s", raiz)
        return pastas

    def periodo_existe(self, periodo: Periodo) -> bool:
        return self._raiz_periodo(periodo).exists()

    def get_pasta_input(self, periodo: Periodo, tipo: str) -> Path:
        return self._raiz_periodo(periodo) / "input" / tipo

    def get_pasta_raw(self, periodo: Periodo) -> Path:
        return self._raiz_appdata(periodo) / "raw"

    def get_pasta_resultados(self, periodo: Periodo) -> Path:
        return self._raiz_periodo(periodo) / "resultados"

    def _raiz_periodo(self, periodo: Periodo) -> Path:
        return settings.WORKSPACE_ROOT / str(periodo.ano) / periodo.mes_formatado

    def _raiz_appdata(self, periodo: Periodo) -> Path:
        return settings.DATA_PATH / str(periodo.ano) / periodo.mes_formatado