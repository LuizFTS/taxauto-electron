from fastapi import APIRouter, status

from core.di.container import get_cancelled_invoices_usecase
from modules.automation.application.dto.cancelled_invoices_dto import CancelledInvoicesDTO
from modules.automation.utils.selenium_driver import SeleniumDriver

router = APIRouter()


@router.post("/cancelled-invoices/run", status_code=status.HTTP_204_NO_CONTENT)
def cancelled_invoices(data: CancelledInvoicesDTO):
    driver = SeleniumDriver(data.save_path)
    usecase = get_cancelled_invoices_usecase(driver)
    usecase.execute(data)
