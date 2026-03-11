from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

from modules.automation.application.dto.livros_fiscais_dto import (
    LivrosFiscaisDTO,
    LivrosFiscaisTasksDTO,
)
from modules.automation.application.usecases.run_livros_fiscais import RunLivrosFiscaisUseCase

router = APIRouter()


class TaskRequest(BaseModel):
    open_book: bool
    update_book: bool
    close_book: bool
    save_spreadsheet: bool
    save_pdf: bool


class LivrosFiscaisRequest(BaseModel):
    start_date: str
    end_date: str
    filiais: List[str]
    book_type: str
    tasks: TaskRequest


@router.post("/livros-fiscais/run")
def run_livros_fiscais(data: LivrosFiscaisRequest):

    dto = LivrosFiscaisDTO(
        start_date=data.start_date,
        end_date=data.end_date,
        filiais=data.filiais,
        book_type=data.book_type,
        tasks=LivrosFiscaisTasksDTO(**data.tasks.model_dump()),
    )

    usecase = RunLivrosFiscaisUseCase()
    return usecase.execute(dto)
