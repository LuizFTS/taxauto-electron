from datetime import datetime

from modules.automation.application.automation_runner import AutomationRunner
from modules.automation.application.dto.tax_assessment_report_dto import TaxAssessmentReportDTO
from modules.automation.features.state.automation_state import AutomationState
from modules.automation.features.tax_assessment.orchestrator.save_assessment_report_orchestrator import (
    SaveAssessmentReportOrchestrator,
)


class RunTaxAssessmentUseCase:
    def __init__(self, orchestrator: SaveAssessmentReportOrchestrator, automation_state: AutomationState):
        self.orchestrator = orchestrator
        self.automation_state = automation_state

    def execute(self, dto: TaxAssessmentReportDTO):

        if len(dto.filiais) == 0:
            raise Exception("Selecione pelo menos uma filial para prosseguir.")

        try:
            datetime.strptime(dto.date, "%d/%m/%Y")

        except ValueError:
            raise Exception("Formato de data inválido. Use DD/MM/AAAA.")

        runner = AutomationRunner(self.automation_state)
        runner.run(self.orchestrator.execute, dto)
