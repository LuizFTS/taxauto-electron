from datetime import datetime

from modules.automation.application.dto.cancelled_invoices_dto import CancelledInvoicesDTO
from modules.automation.automations.cancelled_tax_invoices.orchestrator.get_cancelled_report_orchestrator import (
    GetCancelledReportOrchestrator,
)


class CancelledInvoicesUseCase:
    def __init__(
        self,
        get_cancelled_report_orchestrator: GetCancelledReportOrchestrator,
    ):
        self.orchestrator = get_cancelled_report_orchestrator

    def execute(self, dto: CancelledInvoicesDTO):
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
        )
