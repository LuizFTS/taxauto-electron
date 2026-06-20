from fastapi import APIRouter, status

from core.di.container import get_cancelled_invoices_usecase
from modules.automation.application.dto.cancelled_invoices_dto import (
    CancelledInvoicesDTO,
    ValidateFileDTO,
    ValidateFileResponseDTO,
)
from modules.automation.application.usecases.validate_cancelled_invoices_file_usecase import (
    ValidateCancelledInvoicesFileUseCase,
)

router = APIRouter()


@router.post("/cancelled-invoices/run", status_code=status.HTTP_204_NO_CONTENT)
def cancelled_invoices(data: CancelledInvoicesDTO):
    usecase = get_cancelled_invoices_usecase()
    usecase.execute(data)


@router.post("/cancelled-invoices/validate-file", response_model=ValidateFileResponseDTO)
def validate_file(data: ValidateFileDTO):
    usecase = ValidateCancelledInvoicesFileUseCase()
    return usecase.execute(data)
