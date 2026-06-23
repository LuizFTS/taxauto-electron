from core.di.data_process_provider import get_audit_cancelled_invoices_usecase
from modules.automation.application.usecases.cancelled_invoices_flow_usecase import (
    CancelledInvoicesFlowUseCase,
)
from modules.automation.application.usecases.cancelled_invoices_usecase import (
    CancelledInvoicesUseCase,
)
from modules.automation.application.usecases.download_xmls_usecase import (
    DownloadXmlsUseCase,
)
from modules.automation.application.usecases.merge_excel_files_usecase import (
    MergeExcelFilesUseCase,
)
from modules.automation.application.usecases.run_livros_fiscais import (
    RunLivrosFiscaisUseCase,
)
from modules.automation.features.cancelled_tax_invoices.download_report import (
    DownloadReport,
)
from modules.automation.features.cancelled_tax_invoices.generate_report import (
    GenerateReport,
)
from modules.automation.features.cancelled_tax_invoices.navigation import (
    Navigation as CancelledReportNavigation,
)
from modules.automation.features.cancelled_tax_invoices.orchestrator import (
    Orchestrator as CancelledReportOrchestrator,
)
from modules.automation.features.download_xmls.download_service import (
    DownloadService as DownloadReportServiceDownloadXMLs,
)
from modules.automation.features.download_xmls.navigation import (
    Navigation as NavigateToReportDownloadXMLs,
)
from modules.automation.features.download_xmls.orchestrator import (
    Orchestrator as GetXMLsOrchestrator,
)
from modules.automation.features.download_xmls.unzip_service import (
    UnzipService,
)
from modules.automation.features.merge_excel_files.merge_excel_files_service import (
    MergeExcelFilesService,
)
from modules.automation.features.state.automation_state import AutomationState
from modules.automation.features.tax_reports.navigation import (
    Navigation as TaxReportsNavigation,
)
from modules.automation.features.tax_reports.orchestrator.save_books_orchestrator import (
    SaveBooksOrchestrator,
)
from modules.automation.features.tax_reports.orchestrator.tax_books_orchestrator import (
    TaxBooksOrchestrator,
)
from modules.automation.features.tax_reports.services.close_book import CloseBook
from modules.automation.features.tax_reports.services.open_book import OpenBook
from modules.automation.features.tax_reports.services.save_pdf import SavePDF
from modules.automation.features.tax_reports.services.save_spreadsheet import (
    SaveSpreadsheet,
)
from modules.automation.features.tax_reports.services.update_book import (
    UpdateBook,
)
from modules.automation.features.tax_reports.state.book_state import BookState
from modules.automation.infrastructure.browser import (
    BrowserSession,
)
from modules.automation.infrastructure.erp_session import ERPSession

_generate_report_service = GenerateReport()
_merge_excel_files_service = MergeExcelFilesService()
_automation_state = AutomationState()
_open_book = OpenBook(_automation_state)
_update_book = UpdateBook(_automation_state)
_close_book = CloseBook(_automation_state)
_book_state = BookState()
_unzip_files = UnzipService()
_navigate_to_livros_fiscais = TaxReportsNavigation()
_erp_session = ERPSession()
_save_pdf = SavePDF(_erp_session, _automation_state)
_save_spreadsheet = SaveSpreadsheet(_erp_session, _automation_state)


def get_automation_state():
    return _automation_state


def get_browser_session():
    return BrowserSession()


def get_navigate_to_report():
    return CancelledReportNavigation()


def get_download_report():
    return DownloadReport()


def get_navigate_to_report_download_xmls():
    return NavigateToReportDownloadXMLs()


def get_download_report_download_xmls():
    return DownloadReportServiceDownloadXMLs()


def get_save_books_orchestrator():
    return SaveBooksOrchestrator(
        _erp_session,
        _automation_state,
        _merge_excel_files_service,
        _save_pdf,
        _save_spreadsheet,
    )


def get_livros_fiscais_orchestrator():
    return TaxBooksOrchestrator(
        _automation_state,
        _merge_excel_files_service,
        _open_book,
        _update_book,
        _close_book,
        _book_state,
        _navigate_to_livros_fiscais,
        _erp_session,
        get_save_books_orchestrator(),
    )


def get_cancelled_report_orchestrator():
    return CancelledReportOrchestrator(
        get_browser_session(),
        get_navigate_to_report(),
        get_download_report(),
        _generate_report_service,
    )


def get_xmls_orchestrator():
    return GetXMLsOrchestrator(
        get_browser_session(),
        get_navigate_to_report_download_xmls(),
        get_download_report_download_xmls(),
        _unzip_files,
    )


def get_run_livros_fiscais_usecase():
    return RunLivrosFiscaisUseCase(get_livros_fiscais_orchestrator(), _automation_state)


def get_merge_excel_files_usecase():
    return MergeExcelFilesUseCase(_merge_excel_files_service)


def get_cancelled_invoices_usecase():
    return CancelledInvoicesUseCase(
        get_cancelled_report_orchestrator(),
    )


def get_cancelled_invoices_flow_usecase():
    return CancelledInvoicesFlowUseCase(
        get_livros_fiscais_orchestrator(),
        get_cancelled_invoices_usecase(),
        _merge_excel_files_service,
        get_audit_cancelled_invoices_usecase(),
    )


def get_download_xmls_usecase():
    return DownloadXmlsUseCase(
        get_xmls_orchestrator(),
    )
