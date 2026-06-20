from datetime import datetime

from modules.automation.application.automation_runner import AutomationRunner
from modules.automation.application.dto.livros_fiscais_dto import LivrosFiscaisDTO
from modules.automation.features.state.automation_state import AutomationState
from modules.automation.features.tax_reports.orchestrator.tax_books_orchestrator import (
    TaxBooksOrchestrator,
)


class RunLivrosFiscaisUseCase:
    def __init__(self, orchestrator: TaxBooksOrchestrator, automation_state: AutomationState):
        self.orchestrator = orchestrator
        self.automation_state = automation_state

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

            """ periodos = (
                pd.date_range(start=date_start, end=date_end, freq='MS')
                .strftime('%m/%Y')
                .tolist()
            ) """

        except ValueError:
            raise Exception("Formato de data inválido. Use DD/MM/AAAA.")

        if date_end < date_start:
            raise ValueError("A data final não pode ser menor que a data inicial.")

        runner = AutomationRunner(self.automation_state)
        runner.run(self.orchestrator.execute, dto)
