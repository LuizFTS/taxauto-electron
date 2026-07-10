import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List

from modules.automation.features.cancelled_tax_invoices.download_report import (
    DownloadReport,
)
from modules.automation.features.cancelled_tax_invoices.generate_report import (
    GenerateReport,
)
from modules.automation.features.cancelled_tax_invoices.navigation import (
    Navigation,
)
from modules.automation.infrastructure.browser import (
    BrowserSession,
)
from modules.automation.infrastructure.cleanup_chromedriver import cleanup_chromedriver
from modules.automation.infrastructure.selenium import SeleniumDriver

logger = logging.getLogger(__name__)


class Orchestrator:
    def __init__(
        self,
        browser_session: BrowserSession,
        navigate_to_report: Navigation,
        download_report: DownloadReport,
        generate_report: GenerateReport,
    ):
        self.browser_session = browser_session
        self.navigate_to_report = navigate_to_report
        self.download_report = download_report
        self.generate_report = generate_report

    def _process_filial(
        self,
        filial: str,
        parent_directory: str,
        start_date: str,
        end_date: str,
        login: str,
        password: str,
    ):
        logger.info(f"[Filial {filial}] Iniciando download do relatório")
        logger.debug(f"[Filial {filial}] Parâmetros: start_date={start_date}, end_date={end_date}")
        driver = SeleniumDriver(parent_directory, headless=True)

        browser_session = self.browser_session.__class__()
        navigate_to_report = self.navigate_to_report.__class__()
        download_report = self.download_report.__class__()

        try:
            browser_session.execute(driver, login, password)
            navigate_to_report.execute(driver, int(filial))
            path = download_report.execute(
                driver,
                parent_directory,
                int(filial),
                start_date,
                end_date,
            )
            self.generate_report.execute(path, str(int(filial)).zfill(2))
            return filial, None
        except Exception as e:
            logger.error(f"[Filial {filial}] Erro ao gerar relatório: {e}", exc_info=True)
            return filial, e
        finally:
            try:
                driver.quit()
            except Exception as e:
                logger.error(f"[Filial {filial}] Erro ao fechar driver: {e}", exc_info=True)
                pass

    def execute(
        self,
        output_dir: str,
        filiais: List[str],
        start_date: str,
        end_date: str,
        login: str,
        password: str,
        max_workers: int = 1,
    ):
        date_string = f"{str(start_date.replace('/', ''))}_{str(end_date.replace('/', ''))}"

        parent_directory = os.path.join(output_dir, date_string)

        if os.path.exists(parent_directory):
            i = 1
            while os.path.exists(parent_directory + f"_{i}"):
                i += 1
            parent_directory = parent_directory + f"_{i}"

        # Create parent folder if it doesn't exist
        os.makedirs(parent_directory, exist_ok=True)

        errors = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(
                    self._process_filial,
                    filial,
                    parent_directory,
                    start_date,
                    end_date,
                    login,
                    password,
                ): filial
                for filial in filiais
            }

            for future in as_completed(futures):
                filial, error = future.result()
                if error:
                    errors.append((filial, error))

        cleanup_chromedriver()

        if errors:
            logging.error(f"{len(errors)} filiais falharam")
            for filial, error in errors:
                logging.error(f"Filial {filial} falhou com o erro: {error}")
        else:
            logging.info("Todos os filiais foram processados com sucesso")
