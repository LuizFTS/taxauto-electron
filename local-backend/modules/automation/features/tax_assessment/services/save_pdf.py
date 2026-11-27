from time import sleep

import nazm as a

from modules.automation.features.tax_assessment.utils.download_erp_pdf import (
    cleanup_existing_report_tabs,
    download_erp_pdf,
)
from modules.automation.features.tax_assessment.utils.download_erp_pdf_edge import (
    cleanup_existing_report_tabs_edge,
    download_erp_pdf_edge,
)
from modules.automation.features.tax_assessment.utils.get_default_browser import (
    get_default_browser,
)
from modules.automation.infrastructure.erp_session import ERPSession


class SavePDF:
    def __init__(self, session: ERPSession, state):
        self.session = session
        self.state = state
        self.browser = get_default_browser()

    def execute(self, filial, date, save_path, first_round):

        # Get month + year from date
        period = date[3:5] + date[6:10]

        company = "2" if int(filial) >= 70 else "1"
        self.state.check()
        if first_round:
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

        a.type("ICM")

        # Fill start date
        a.press("tab", 2)
        a.type(period)

        # Fill end date
        a.press("tab")
        a.type(period)

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
        a.press("tab", 3)
