from datetime import datetime

from modules.automation.application.dto.download_xmls_dto import DownloadXmlsDTO
from modules.automation.features.download_xmls.orchestrator import (
    Orchestrator,
)


class DownloadXmlsUseCase:
    def __init__(
        self,
        Orchestrator: Orchestrator,
    ):
        self.orchestrator = Orchestrator

    def execute(self, dto: DownloadXmlsDTO):
        if len(dto.filiais) == 0:
            raise Exception("Selecione pelo menos uma filial para prosseguir.")

        try:
            date_start = datetime.strptime(dto.start_date, "%d/%m/%Y")
            date_end = datetime.strptime(dto.end_date, "%d/%m/%Y")
        except ValueError:
            raise Exception("Formato de data inválido. Use DD/MM/AAAA.")

        if date_end < date_start:
            raise ValueError("A data final não pode ser menor que a data inicial.")

        self.orchestrator.execute(
            dto.save_path,
            dto.filiais,
            dto.start_date,
            dto.end_date,
            dto.login,
            dto.password,
            dto.tipo_documento,
            dto.tipo_operacao,
        )
