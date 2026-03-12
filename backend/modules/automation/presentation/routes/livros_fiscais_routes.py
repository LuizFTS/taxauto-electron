from fastapi import APIRouter, status

from modules.automation.application.dto.livros_fiscais_dto import (
    LivrosFiscaisDTO,
    LivrosFiscaisTasksDTO,
)
from modules.automation.application.usecases.run_livros_fiscais import RunLivrosFiscaisUseCase

router = APIRouter()


@router.post("/livros-fiscais/run", status_code=status.HTTP_204_NO_CONTENT)
def run_livros_fiscais(data: LivrosFiscaisDTO):

    dto = LivrosFiscaisDTO(
        start_date=data.start_date,
        end_date=data.end_date,
        filiais=data.filiais,
        book_type=data.book_type,
        save_path=data.save_path,
        tasks=LivrosFiscaisTasksDTO(
            data.tasks.open_book,
            data.tasks.update_book,
            data.tasks.close_book,
            data.tasks.save_spreadsheet,
            data.tasks.save_pdf,
        ),
    )

    usecase = RunLivrosFiscaisUseCase()
    usecase.execute(dto)
