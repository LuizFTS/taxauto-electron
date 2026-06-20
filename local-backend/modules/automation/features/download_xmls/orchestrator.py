import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List

from modules.automation.features.download_xmls.download_service import DownloadService
from modules.automation.features.download_xmls.navigation import (
    Navigation,
)
from modules.automation.features.download_xmls.unzip_service import UnzipService
from modules.automation.infrastructure.browser import BrowserSession
from modules.automation.infrastructure.cleanup_chromedriver import cleanup_chromedriver
from modules.automation.infrastructure.selenium import SeleniumDriver


class Orchestrator:
    def __init__(
        self,
        browser_session: BrowserSession,
        navigate_to_report: Navigation,
        download_report: DownloadService,
        unzip_files: UnzipService,
    ):
        self.browser_session = browser_session
        self.navigate_to_report = navigate_to_report
        self.download_report = download_report
        self.unzip_files = unzip_files

    def _process_filial(
        self,
        filial: str,
        parent_directory: str,
        start_date: str,
        end_date: str,
        login: str,
        password: str,
        tipo_documento: int,
        tipo_operacao: int,
    ):
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
                tipo_documento,
                tipo_operacao,
            )
            self.unzip_files.execute(path)
            print(f"Filial {filial} processado com sucesso")
            return filial, None
        except Exception as e:
            print(e)
            return filial, e
        finally:
            try:
                driver.quit()
            except Exception as e:
                print(e)
                pass

    def execute(
        self,
        output_dir: str,
        filiais: List[str],
        start_date: str,
        end_date: str,
        login: str,
        password: str,
        tipo_documento: int,
        tipo_operacao: int,
        max_workers: int = 7,
    ):

        # Does the parent folder exist? if it does add the number of the folder,
        # if folder one exists create a folder '_2' and so on
        tp_documento = "NFE" if tipo_documento == 1 else "CTE"
        tp_operacao = "SAIDA" if tipo_operacao == 1 else "ENTRADA"

        date_string = f"{str(start_date.replace('/', ''))}_{str(end_date.replace('/', ''))}"

        parent_folder = f"{date_string}_{tp_documento}_{tp_operacao}"
        parent_directory = os.path.join(output_dir, parent_folder)

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
                    tipo_documento,
                    tipo_operacao,
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

        """ for filial in filiais:
            self.navigate_to_report.execute(int(filial))
            path = self.download_report.execute(
                parent_directory, int(filial), start_date, end_date, tipo_documento, tipo_operacao
            )
            self.unzip_files.execute(path) """
