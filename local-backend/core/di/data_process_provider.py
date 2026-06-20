from modules.data_process.application.usecases.audit_cancelled_invoices_usecase import (
    AuditCancelledInvoicesUseCase,
)
from modules.data_process.application.usecases.delete_audit_report_usecase import (
    DeleteAuditReportUseCase,
)
from modules.data_process.application.usecases.list_audit_reports_usecase import (
    ListAuditReportsUseCase,
)
from modules.data_process.application.usecases.read_audit_report_usecase import (
    ReadAuditReportUseCase,
)
from modules.data_process.audits.cancelled_invoices.services.load_and_merge_date_service import (
    LoadAndMergeDataService,
)


def get_delete_audit_report_usecase():
    return DeleteAuditReportUseCase()


def get_list_audit_reports_usecase():
    return ListAuditReportsUseCase()


def get_read_audit_report_usecase():
    return ReadAuditReportUseCase()


def get_load_and_merge_data_service():
    return LoadAndMergeDataService()


def get_audit_cancelled_invoices_usecase():
    return AuditCancelledInvoicesUseCase(get_load_and_merge_data_service())
