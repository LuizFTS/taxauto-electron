from time import sleep

import nazm as a
import nazm.capture as c

from modules.automation.automations.livros_fiscais.utils.download_erp_pdf import (
    cleanup_existing_report_tabs,
    download_erp_pdf,
)


class SavePDFService:

    def execute(self, filial, book_type, start_date, end_date):
        t = c.load_templates()

        company = "2" if int(filial) >= 70 else "1"

        sleep(1)
        cleanup_existing_report_tabs()
        a.click(t.livro_printer)
        a.wait_cursor_normal()

        # Fill company field
        a.click(t.exit, -740, -620)
        a.type(company)

        # Fill branch field
        a.press("tab")
        a.type(str(int(filial)))

        # Select book type
        a.press("tab")
        if book_type == "entrada":
            a.press("down")

        # Fill start date
        a.click(t.exit, 13, -115)
        a.type("start_date")

        # Fill end date
        a.click(t.exit, 9, -52)
        a.type("end_date")

        # Open pdf in Chrome
        a.press("tab")
        a.press("space")
        download_erp_pdf()
