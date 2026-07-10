import os
import shutil
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

from modules.automation.application.dto.cancelled_invoices_dto import CancelledInvoicesDTO
from modules.automation.application.dto.cancelled_invoices_dto_flow import CancelledInvoicesFlowDTO
from modules.automation.application.dto.livros_fiscais_dto import (
    LivrosFiscaisDTO,
    LivrosFiscaisTasksDTO,
)
from modules.automation.application.usecases.cancelled_invoices_usecase import (
    CancelledInvoicesUseCase,
)
from modules.automation.features.merge_excel_files.merge_excel_files_service import (
    MergeExcelFilesService,
)
from modules.automation.features.tax_reports.orchestrator.tax_books_orchestrator import (
    TaxBooksOrchestrator,
)
from modules.data_process.application.usecases.audit_cancelled_invoices_usecase import (
    AuditCancelledInvoicesUseCase,
)


class CancelledInvoicesFlowUseCase:
    def __init__(
        self,
        taxBooksOrchestrator: TaxBooksOrchestrator,
        cancelledInvoicesUseCase: CancelledInvoicesUseCase,
        mergeSpreadsheets: MergeExcelFilesService,
        auditCancelledInvoicesUseCase: AuditCancelledInvoicesUseCase,
    ):
        self.cancelledInvoicesUseCase = cancelledInvoicesUseCase
        self.taxBooksOrchestrator = taxBooksOrchestrator
        self.mergeSpreadsheets = mergeSpreadsheets
        self.auditCancelledInvoicesUseCase = auditCancelledInvoicesUseCase

    def _create_livros_fiscais_dto(
        self,
        dto: CancelledInvoicesFlowDTO,
        path: str,
        update_book: bool = True,
        close_book: bool = True,
    ):
        tasks = LivrosFiscaisTasksDTO(
            open_book=False,
            update_book=update_book,
            close_book=close_book,
            save_spreadsheet=True,
            save_pdf=False,
        )

        return LivrosFiscaisDTO(dto.start_date, dto.end_date, dto.filiais, "saida", tasks, path)

    def _create_cancelled_invoices_dto(self, dto: CancelledInvoicesFlowDTO, path: str):
        return CancelledInvoicesDTO(
            dto.start_date,
            dto.end_date,
            dto.filiais,
            path,
            dto.login,
            dto.password,
        )

    def execute(self, dto: CancelledInvoicesFlowDTO):
        base = os.getenv("LOCALAPPDATA")

        if not base:
            raise RuntimeError("LOCALAPPDATA não encontrado")

        temp_dir = Path(base) / "TaxAuto" / "Temp2"

        if temp_dir.exists():
            shutil.rmtree(temp_dir)

        temp_dir.mkdir(parents=True, exist_ok=True)

        if len(dto.filiais) == 0:
            raise Exception("Selecione pelo menos uma filial para prosseguir.")

        try:
            date_start = datetime.strptime(dto.start_date, "%d/%m/%Y")
            date_end = datetime.strptime(dto.end_date, "%d/%m/%Y")
        except ValueError:
            raise Exception("Formato de data inválido. Use DD/MM/AAAA.")

        if date_end < date_start:
            raise ValueError("A data final não pode ser menor que a data inicial.")

        with ThreadPoolExecutor(max_workers=2) as executor:
            update_book = False
            close_book = False
            for task in dto.tasks:
                if task.code == "atualizar-livro-saida":
                    update_book = True
                elif task.code == "fechar-livro-saida":
                    close_book = True

            future_livros = executor.submit(
                self.taxBooksOrchestrator.execute,
                self._create_livros_fiscais_dto(
                    dto, str(temp_dir), update_book=update_book, close_book=close_book
                ),
            )

            future_cancelled_invoices = executor.submit(
                self.cancelledInvoicesUseCase.execute,
                self._create_cancelled_invoices_dto(dto, str(temp_dir)),
            )

            future_livros.result()
            future_cancelled_invoices.result()

        # Merge spreadsheets
        CancelledInvoicesReportsFolderPath = (
            Path(temp_dir)
            / f"{str(dto.start_date.replace('/', ''))}_{str(dto.end_date.replace('/', ''))}"
        )

        # for each .xlsx file in the folder, store it in a list of strings
        spreadsheets = [str(file) for file in CancelledInvoicesReportsFolderPath.glob("*.xlsx")]

        self.mergeSpreadsheets.execute(spreadsheets, str(temp_dir))

        book_path = str(
            temp_dir
            / f"SAIDA_{dto.start_date.replace('/', '')}_{dto.end_date.replace('/', '')}.xlsx"
        )
        portal_path = str(temp_dir / "CONSOLIDADO.xlsx")
        return self.auditCancelledInvoicesUseCase.execute(book_path, portal_path)
