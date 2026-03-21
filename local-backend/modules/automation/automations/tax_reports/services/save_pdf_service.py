from time import sleep

import nazm as a

from modules.automation.automations.tax_reports.navigation.erp_session import ERPSession
from modules.automation.automations.tax_reports.utils.download_erp_pdf import (
    cleanup_existing_report_tabs,
    download_erp_pdf,
)
from modules.automation.automations.tax_reports.utils.download_erp_pdf_edge import (
    cleanup_existing_report_tabs_edge,
    download_erp_pdf_edge,
)
from modules.automation.automations.tax_reports.utils.get_default_browser import (
    get_default_browser,
)


class SavePDFService:

    def __init__(self, session: ERPSession, state):
        self.session = session
        self.state = state
        self.browser = get_default_browser()

    def execute(self, filial, book_type, start_date, end_date, save_path, first_round):
        company = "2" if int(filial) >= 70 else "1"
        self.state.check()
        if first_round:
            sleep(0.3)

            if self.browser == "chrome":
                cleanup_existing_report_tabs()
            else:
                cleanup_existing_report_tabs_edge()
            self.state.check()
            self.session.focus()

        # Fill company field
        a.type(company)
        a.press("tab")
        self.state.check()

        # Fill branch field
        a.type(str(int(filial)))
        a.press("tab")
        self.state.check()

        # Select book type
        if book_type == "entrada":
            a.press("down")
            a.press("tab")
            self.state.check()
            if first_round:
                a.press("space")
            a.press("tab", 12)
            a.press("up")
            a.press("tab", 3)

        if book_type == "saida":
            a.press("tab", 10)
            a.press("up")
            a.press("tab", 3)
        self.state.check()

        if first_round:
            a.type(start_date)

        a.press("tab")

        if first_round:
            a.type(end_date)

        self.state.check()

        # Open pdf in Chrome
        a.press("tab")
        a.press("space")
        self.state.check()
        if self.browser == "chrome":
            download_erp_pdf(save_path)
        else:
            download_erp_pdf_edge(save_path)
        self.state.check()

        self.session.focus()
        sleep(0.5)
        a.press("tab", 3)
