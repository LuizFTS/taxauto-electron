from datetime import datetime

from core.di.container import automation_state
from modules.automation.application.automation_runner import AutomationRunner
from modules.automation.application.dto.livros_fiscais_dto import LivrosFiscaisDTO
from modules.automation.automations.tax_reports.orchestrator.livros_fiscais_orchestrator import (
    LivrosFiscaisOrchestrator,
)


class RunLivrosFiscaisUseCase:

    def execute(self, dto: LivrosFiscaisDTO):

        if dto.book_type not in ["entrada", "saida"]:
            raise Exception(f'Livro "{dto.book_type}" informado é incompatível.')

        if len(dto.filiais) == 0:
            raise Exception("Selecione pelo menos uma filial para prosseguir.")

        if not any(dto.tasks.__dict__.values()):
            raise Exception("Selecione pelo menos uma tarefa para prosseguir.")

        try:
            date_start = datetime.strptime(dto.start_date, "%d/%m/%Y")
            date_end = datetime.strptime(dto.end_date, "%d/%m/%Y")
        except ValueError:
            raise Exception("Formato de data inválido. Use DD/MM/AAAA.")

        if date_end < date_start:
            raise ValueError("A data final não pode ser menor que a data inicial.")

        orchestrator = LivrosFiscaisOrchestrator(automation_state)

        runner = AutomationRunner(automation_state)
        runner.run(orchestrator.execute, dto)
