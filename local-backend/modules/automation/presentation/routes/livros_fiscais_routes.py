from fastapi import APIRouter, status

from modules.automation.application.dto.livros_fiscais_dto import LivrosFiscaisDTO
from modules.automation.application.usecases.run_livros_fiscais import RunLivrosFiscaisUseCase

router = APIRouter()


@router.post("/livros-fiscais/run", status_code=status.HTTP_204_NO_CONTENT)
def run_livros_fiscais(data: LivrosFiscaisDTO):
    usecase = RunLivrosFiscaisUseCase()
    usecase.execute(data)
