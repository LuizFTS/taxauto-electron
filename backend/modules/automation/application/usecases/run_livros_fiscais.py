from modules.automation.application.dto.livros_fiscais_dto import LivrosFiscaisDTO
from modules.automation.automations.livros_fiscais.orchestrator.livros_fiscais_orchestrator import (
    LivrosFiscaisOrchestrator,
)


class RunLivrosFiscaisUseCase:

    def execute(self, dto: LivrosFiscaisDTO):

        orchestrator = LivrosFiscaisOrchestrator()

        return orchestrator.execute(dto)