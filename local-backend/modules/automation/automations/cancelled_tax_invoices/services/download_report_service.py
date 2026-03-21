import os
import subprocess
from urllib.parse import quote

from selenium.webdriver.common.by import By

from modules.automation.utils.selenium_driver import SeleniumDriver


class DownloadReportService:
    def __init__(self, driver: SeleniumDriver):
        self.driver = driver

    def execute(self, output_dir: str, filial: int, start_date: str, end_date: str):

        d = self.driver.driver
        print("Iniciando download do relatório...")

        # 1. Extrair os dados dinâmicos do Selenium
        jsessionid = ""
        for cookie in d.get_cookies():
            if cookie["name"] == "JSESSIONID":
                jsessionid = cookie["value"]
                break

        view_state = d.find_element(By.NAME, "javax.faces.ViewState").get_attribute("value")
        file_path = os.path.join(
            output_dir,
            f"{str(filial).zfill(2)}_{start_date.replace('/', '')}_{end_date.replace('/', '')}_CANCELADAS.xls",
        )

        data_inicio_encoded = quote(start_date, safe="")
        data_fim_encoded = quote(end_date, safe="")

        # 2. Montar o script PowerShell (usando f-string para inserir as variáveis)
        # Nota: Usamos @' ... '@ para strings de múltiplas linhas no PowerShell
        ps_script = f"""
        $session = New-Object Microsoft.PowerShell.Commands.WebRequestSession
        $session.UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
        $cookie = New-Object System.Net.Cookie("JSESSIONID", "{jsessionid}", "/", "100.126.64.15")
        $session.Cookies.Add($cookie)

        $body = "formCadastro=formCadastro&formCadastro%3AbtnGerarRelatorio=&formCadastro%3AdtPeriodoInicio_input={data_inicio_encoded}&formCadastro%3AdtPeriodoFinal_input={data_fim_encoded}&formCadastro%3Arelatorio=STATUS_NFE&formCadastro%3Aj_idt83=0&formCadastro%3Astatus=2&formCadastro%3Astatus=3&formCadastro%3Astatus=4&formCadastro%3Astatus=5&formCadastro%3AtpDoc=XLSX&formCadastro%3ArelatorioTable%3Atable%3Aj_idt104%3Afilter=&formCadastro%3ArelatorioTable%3Atable_selection=20&formCadastro%3ArelatorioTable%3Atable_scrollState=0%2C0&javax.faces.ViewState={view_state}"

        Invoke-WebRequest -UseBasicParsing -Uri "http://100.126.64.15:8080/adged/relatorio.xhtml" `
        -Method "POST" `
        -WebSession $session `
        -ContentType "application/x-www-form-urlencoded" `
        -Body $body `
        -OutFile "{file_path}"
        """

        # 3. Executar o PowerShell via Python
        try:
            subprocess.run(["powershell", "-Command", ps_script], capture_output=True, text=True)
            print("Relatório gerado com sucesso!")
        except Exception as e:
            print(e)
            raise Exception("Erro ao gerar relatório")
