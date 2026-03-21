from typing import List

from modules.automation.automations.cancelled_tax_invoices.navigation.browser_session import (
    BrowserSession,
)
from modules.automation.automations.cancelled_tax_invoices.navigation.navigate_to_report import (
    NavigateToReport,
)
from modules.automation.automations.cancelled_tax_invoices.services.download_report_service import (
    DownloadReportService,
)


class GetCancelledReportOrchestrator:
    def __init__(
        self,
        browser_session: BrowserSession,
        navigate_to_report: NavigateToReport,
        download_report: DownloadReportService,
    ):
        self.browser_session = browser_session
        self.navigate_to_report = navigate_to_report
        self.download_report = download_report

    def execute(
        self,
        output_dir: str,
        filiais: List[str],
        start_date: str,
        end_date: str,
        login: str,
        password: str,
    ):
        self.browser_session.execute(login, password)

        for filial in filiais:
            self.navigate_to_report.execute(int(filial))
            self.download_report.execute(output_dir, int(filial), start_date, end_date)
