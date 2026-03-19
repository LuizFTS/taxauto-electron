from modules.automation.application.dto.merge_excel_files_dto import MergeExcelFilesDTO
from modules.automation.automations.merge_excel_files.services.merge_excel_files_service import (
    MergeExcelFilesService,
)


class MergeExcelFilesUseCase:

    def __init__(self, merge_excel_files_service: MergeExcelFilesService):
        self.merge_excel_files_service = merge_excel_files_service

    def execute(self, dto: MergeExcelFilesDTO):

        if not dto.paths:
            raise ValueError("Nenhum arquivo informado.")

        if not dto.output_path:
            raise ValueError("Nenhum diretório de saída informado.")

        self.merge_excel_files_service.execute(dto.paths, dto.output_path)
