from fastapi import APIRouter, status

from core.di.container import get_run_livros_fiscais_usecase
from modules.automation.application.dto.livros_fiscais_dto import LivrosFiscaisDTO

router = APIRouter()


@router.post("/tax-reports/run", status_code=status.HTTP_204_NO_CONTENT)
def run_tax_reports(data: LivrosFiscaisDTO):
    usecase = get_run_livros_fiscais_usecase()
    usecase.execute(data)
