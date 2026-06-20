from typing import List

from fastapi import APIRouter, Query, status

from core.di.container import (
    get_audit_cancelled_invoices_usecase,
    get_delete_audit_report_usecase,
    get_list_audit_reports_usecase,
    get_read_audit_report_usecase,
)
from modules.data_process.application.dto.audit_cancelled_invoice_request import (
    AuditCancelledInvoiceRequest,
)
from modules.data_process.application.dto.audit_report_entry import AuditReportEntry
from modules.data_process.domain.entities.AuditDiscrepancy import AuditSummary

router = APIRouter()


@router.post("/cancelled-invoices/run", status_code=status.HTTP_200_OK, response_model=AuditSummary)
def cancelled_invoices(dto: AuditCancelledInvoiceRequest):
    """
    Executa a auditoria de notas fiscais canceladas.
    """
    usecase = get_audit_cancelled_invoices_usecase()
    return usecase.execute(dto.book_path, dto.portal_path)


@router.get(
    "/cancelled-invoices/report",
    status_code=status.HTTP_200_OK,
    response_model=AuditSummary,
)
def get_audit_report(report_name: str = Query(...)):
    """
    Lê o relatório de auditoria de notas fiscais canceladas.
    """
    usecase = get_read_audit_report_usecase()
    return usecase.execute(report_name)


@router.get(
    "/cancelled-invoices/reports",
    status_code=status.HTTP_200_OK,
    response_model=List[AuditReportEntry],
)
def list_audit_reports():
    """
    Lista os relatórios de auditoria de notas fiscais canceladas.
    """
    usecase = get_list_audit_reports_usecase()
    return usecase.execute()


@router.delete(
    "/cancelled-invoices/report",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_audit_report(report_name: str = Query(...)):
    """
    Deleta o relatório de auditoria de notas fiscais canceladas.
    """
    usecase = get_delete_audit_report_usecase()
    usecase.execute(report_name)
