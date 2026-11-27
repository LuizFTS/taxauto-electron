from datetime import datetime

from modules.automation.application.automation_runner import AutomationRunner
from modules.automation.application.dto.tax_reports_dto import TaxReportsDTO
from modules.automation.features.state.automation_state import AutomationState
from modules.automation.features.tax_reports.orchestrator.tax_reports_orchestrator import (
    TaxReportsOrchestrator,
)


class RunTaxReportsUseCase:
    def __init__(self, orchestrator: TaxReportsOrchestrator, automation_state: AutomationState):
        self.orchestrator = orchestrator
        self.automation_state = automation_state

    def execute(self, dto: TaxReportsDTO):
        if dto.module not in [
            "ICAN",
            "ICST_NFE",
            "ICST_CTE",
            "ESTORNOS",
            "FRETE",
            "DIFAL_NFE",
            "DIFAL_CTE",
            "FOT",
        ]:
            raise Exception(f'Módulo "{dto.module}" informado é incompatível.')

        if len(dto.filiais) == 0:
            raise Exception("Selecione pelo menos uma filial para prosseguir.")

        try:
            date_start = datetime.strptime(dto.start_date, "%d/%m/%Y")
            date_end = datetime.strptime(dto.end_date, "%d/%m/%Y")

        except ValueError:
            raise Exception("Formato de data inválido. Use DD/MM/AAAA.")

        if date_end < date_start:
            raise ValueError("A data final não pode ser menor que a data inicial.")

        runner = AutomationRunner(self.automation_state)
        runner.run(self.orchestrator.execute, dto)
