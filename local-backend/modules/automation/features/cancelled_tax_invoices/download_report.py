import logging
import os
import subprocess
from time import sleep
from urllib.parse import quote

from selenium.webdriver.common.by import By

from modules.automation.infrastructure.selenium import SeleniumDriver

logger = logging.getLogger(__name__)


class DownloadReport:
    def execute(
        self, driver: SeleniumDriver, output_dir: str, filial: int, start_date: str, end_date: str
    ):
        d = driver.driver
        # Go to Reports section
        d.get("http://100.126.64.15:8080/adged/relatorio.xhtml")
        logger.info(f"[Filial {filial}] Iniciando download do relatório")
        sleep(2)

        # 1. Extrair os dados dinâmicos do Selenium
        jsessionid = ""
        for cookie in d.get_cookies():
            if cookie["name"] == "JSESSIONID":
                jsessionid = cookie["value"]
                break

        view_state = d.find_element(By.NAME, "javax.faces.ViewState").get_attribute("value")

        file_path = os.path.join(
            output_dir,
            f"{str(filial).zfill(2)}_CANCELADAS.xls",
        )

        data_inicio_encoded = quote(start_date, safe="")
        data_fim_encoded = quote(end_date, safe="")

        # 2. Montar o script PowerShell (usando f-string para inserir as variáveis)
        # Nota: Usamos @' ... '@ para strings de múltiplas linhas no PowerShell
        ps_script = f"""
            $baseUrl = "http://100.126.64.15:8080"
            $url = "$baseUrl/adged/relatorio.xhtml"

            # Sessão
            $session = New-Object Microsoft.PowerShell.Commands.WebRequestSession
            $session.UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
            $session.Cookies.Add(
                (New-Object System.Net.Cookie("JSESSIONID", "{jsessionid}", "/", "100.126.64.15"))
            )

            # Body
            $status = "formCadastro%3Astatus=2&formCadastro%3Astatus=3&formCadastro%3Astatus=4&formCadastro%3Astatus=5"

            $body = "formCadastro=formCadastro&formCadastro%3AbtnGerarRelatorio=&formCadastro%3AdtPeriodoInicio_input={data_inicio_encoded}&formCadastro%3AdtPeriodoFinal_input={data_fim_encoded}&formCadastro%3Arelatorio=STATUS_NFE&formCadastro%3Aj_idt83=2&$status&formCadastro%3AtpDoc=XLSX&formCadastro%3ArelatorioTable%3Atable_selection=20&javax.faces.ViewState={view_state}"


            # Request
            Invoke-WebRequest `
                -Uri $url `
                -Method POST `
                -WebSession $session `
                -Headers @{{
                    "Origin"  = $baseUrl
                    "Referer" = $url
                }} `
                -ContentType "application/x-www-form-urlencoded" `
                -Body $body `
                -OutFile "{file_path}"
            """

        # 3. Executar o PowerShell via Python
        try:
            subprocess.run(["powershell", "-Command", ps_script], capture_output=True, text=True)
            logger.info(f"[Filial {filial}] Relatório gerado com sucesso!")
            return file_path
        except Exception as e:
            logger.error(f"[Filial {filial}] Erro ao gerar relatório: {e}", exc_info=True)
            raise Exception("Erro ao gerar relatório")
