from pathlib import Path
from typing import List

from modules.automation.application.dto.merge_excel_files_dto import MergeExcelFilesDTO
from modules.automation.automations.merge_excel_files.services.merge_excel_files_service import (
    MergeExcelFilesService,
)


class MergeExcelFilesUseCase:
    """
    Application use case responsible for orchestrating the merge of Excel/CSV files.

    Responsibilities:
    - Validate input data (DTO)
    - Normalize input paths
    - Delegate execution to domain/service layer
    """

    def __init__(self, merge_excel_files_service: MergeExcelFilesService):
        self._service = merge_excel_files_service

    def execute(self, dto: MergeExcelFilesDTO):
        """
        Executes the merge process.

        :param dto: Input data transfer object
        :return: Path of the generated file
        """
        paths = self._validate_and_normalize_paths(dto.paths)
        output_dir = self._validate_output_path(dto.output_path)

        return self._service.execute(paths, str(output_dir))

        # =========================

    # Validation Layer
    # =========================

    def _validate_and_normalize_paths(self, paths: List[str]) -> List[str]:
        if not paths:
            raise ValueError("Nenhum arquivo informado.")

        normalized_paths: List[str] = []

        for raw_path in paths:
            if not raw_path or not raw_path.strip():
                raise ValueError("Caminho de arquivo inválido.")

            path = Path(raw_path).expanduser().resolve()

            if not path.exists():
                raise FileNotFoundError(f"Arquivo não encontrado: {path}")

            if not path.is_file():
                raise ValueError(f"Caminho não é um arquivo: {path}")

            normalized_paths.append(str(path))

        return normalized_paths

    def _validate_output_path(self, output_path: str) -> Path:
        if not output_path or not output_path.strip():
            raise ValueError("Nenhum diretório de saída informado.")

        path = Path(output_path).expanduser().resolve()

        # Do not require existence — service will handle creation
        if path.exists() and not path.is_dir():
            raise ValueError(f"O caminho de saída não é um diretório: {path}")

        return path
