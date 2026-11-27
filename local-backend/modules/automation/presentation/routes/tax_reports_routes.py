from fastapi import APIRouter, status

from core.di.container import get_run_livros_fiscais_usecase, get_run_tax_reports_usecase, get_run_tax_assessment_usecase
from modules.automation.application.dto.livros_fiscais_dto import LivrosFiscaisDTO
from modules.automation.application.dto.tax_reports_dto import TaxReportsDTO
from modules.automation.application.dto.tax_assessment_report_dto import TaxAssessmentReportDTO

router = APIRouter()


@router.post("/tax-books/run", status_code=status.HTTP_204_NO_CONTENT)
def run_tax_books(data: LivrosFiscaisDTO):
    usecase = get_run_livros_fiscais_usecase()
    usecase.execute(data)


@router.post("/tax-reports/run", status_code=status.HTTP_204_NO_CONTENT)
def run_tax_reports(data: TaxReportsDTO):
    usecase = get_run_tax_reports_usecase()
    usecase.execute(data)


@router.post("/tax-reports/assessment", status_code=status.HTTP_204_NO_CONTENT)
def run_tax_assessment_report(data: TaxAssessmentReportDTO):
    usecase = get_run_tax_assessment_usecase()
    usecase.execute(data)
