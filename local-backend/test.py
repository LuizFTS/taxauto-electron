import os
import subprocess
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from modules.automation.automations.cancelled_tax_invoices.navigation.browser_session import (
    BrowserSession,
)
from modules.automation.automations.cancelled_tax_invoices.navigation.navigate_to_report import (
    NavigateToReport,
)
from modules.automation.automations.cancelled_tax_invoices.orchestrator.get_cancelled_report_orchestrator import (
    GetCancelledReportOrchestrator,
)
from modules.automation.automations.cancelled_tax_invoices.services.download_report_service import (
    DownloadReportService,
)
from modules.automation.utils.selenium_driver import SeleniumDriver


class TestBrowserSession:
    def __init__(self, driver: SeleniumDriver):
        self.driver = driver

    def execute(self):
        self.driver.driver.get("http://100.126.64.15:8080/adged/login.xhtml")
        self._login("DEFIS_AUX20", "lfT#1020304050")

    def _login(self, login: str, password: str):
        d = self.driver
        d.digitar('//*[@id="formLogin:usuario"]', login)
        d.digitar('//*[@id="formLogin:senha"]', password)
        d.clicar('//*[@id="formLogin:btnLogar"]')
        wait = WebDriverWait(d.driver, 10)

        menu_trigger = wait.until(EC.element_to_be_clickable((By.ID, "formLogin:empresa_label")))
        menu_trigger.click()

        filial = 12

        # 2. Espera o painel com as opções aparecer
        panel = wait.until(EC.visibility_of_element_located((By.ID, "formLogin:empresa_panel")))

        if int(filial) < 70:
            # 3. Encontra a opção desejada e clica nela
            opcao_desejada = f"CASA DO ADUBO - FILIAL {filial}"
        else:
            opcao_desejada = f"CASAL COMERCIO E SERVICOS - FILIAL {filial}"
        lista_itens = panel.find_elements(By.CLASS_NAME, "ui-selectonemenu-item")

        for item in lista_itens:
            if item.text.strip() == opcao_desejada:
                item.click()

        d.clicar('//*[@id="formLogin:btnEntrar"]')

        wait.until(
            EC.visibility_of_element_located((By.ID, "globalForm:filtroAvancado:btnPesquisar"))
        )

        # Go to Reports section
        d.driver.get("http://100.126.64.15:8080/adged/relatorio.xhtml")

        d.digitar('//*[@id="formCadastro:dtPeriodoInicio_input"]', "01/03/2026")
        d.digitar('//*[@id="formCadastro:dtPeriodoFinal_input"]', "20/03/2026")

        d.clicar('//*[@id="formCadastro:selectButton"]')

        wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="formCadastro:relatorioTable:table_data"]/tr/td/div')
            )
        )
        d.clicar('//*[@id="formCadastro:relatorioTable:table_data"]/tr/td/div')

        wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="formCadastro:status"]/tbody/tr/td[3]/div/div[2]')
            )
        )
        d.clicar('//*[@id="formCadastro:status"]/tbody/tr/td[3]/div/div[2]')
        d.clicar('//*[@id="formCadastro:status"]/tbody/tr/td[5]/div/div[2]')
        d.clicar('//*[@id="formCadastro:status"]/tbody/tr/td[7]/div/div[2]')
        d.clicar('//*[@id="formCadastro:status"]/tbody/tr/td[9]/div/div[2]')

        # d.clicar('//*[@id="formCadastro:btnGerarRelatorio"]')

        self._download_via_powershell(d.path)
        sleep(10)

    def _logout(self):
        pass

    def _download_via_powershell(self, output_dir):
        d = self.driver.driver
        print("Preparando artilharia PowerShell...")

        # 1. Extrair os dados dinâmicos do Selenium
        jsessionid = ""
        for cookie in d.get_cookies():
            if cookie["name"] == "JSESSIONID":
                jsessionid = cookie["value"]
                break

        view_state = d.find_element(By.NAME, "javax.faces.ViewState").get_attribute("value")
        file_path = os.path.join(output_dir, "relatorio_final.xls")

        # 2. Montar o script PowerShell (usando f-string para inserir as variáveis)
        # Nota: Usamos @' ... '@ para strings de múltiplas linhas no PowerShell
        ps_script = f"""
        $session = New-Object Microsoft.PowerShell.Commands.WebRequestSession
        $session.UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
        $cookie = New-Object System.Net.Cookie("JSESSIONID", "{jsessionid}", "/", "100.126.64.15")
        $session.Cookies.Add($cookie)

        $body = "formCadastro=formCadastro&formCadastro%3AbtnGerarRelatorio=&formCadastro%3AdtPeriodoInicio_input=01%2F03%2F2026&formCadastro%3AdtPeriodoFinal_input=20%2F03%2F2026&formCadastro%3Arelatorio=STATUS_NFE&formCadastro%3Aj_idt83=0&formCadastro%3Astatus=2&formCadastro%3Astatus=3&formCadastro%3Astatus=4&formCadastro%3Astatus=5&formCadastro%3AtpDoc=XLSX&formCadastro%3ArelatorioTable%3Atable%3Aj_idt104%3Afilter=&formCadastro%3ArelatorioTable%3Atable_selection=20&formCadastro%3ArelatorioTable%3Atable_scrollState=0%2C0&javax.faces.ViewState={view_state}"

        Invoke-WebRequest -UseBasicParsing -Uri "http://100.126.64.15:8080/adged/relatorio.xhtml" `
        -Method "POST" `
        -WebSession $session `
        -ContentType "application/x-www-form-urlencoded" `
        -Body $body `
        -OutFile "{file_path}"
        """

        # 3. Executar o PowerShell via Python
        try:
            print("Executando PowerShell...")
            process = subprocess.run(
                ["powershell", "-Command", ps_script], capture_output=True, text=True
            )

            if os.path.exists(file_path) and os.path.getsize(file_path) > 1000:
                print(f"✅ SUCESSO ABSOLUTO! Arquivo salvo: {file_path}")
            else:
                print("❌ O PowerShell executou, mas o arquivo parece inválido ou vazio.")
                print("Erro do PS:", process.stderr)
        except Exception as e:
            print(f"Erro ao chamar o processo: {e}")


if __name__ == "__main__":

    driver = SeleniumDriver(r"C:\Users\lu9887091\Downloads", headless=False)

    browser_session = BrowserSession(driver)
    navigate_to_report = NavigateToReport(driver)
    download_report = DownloadReportService(driver)

    GetCancelledReportOrchestrator(
        driver, browser_session, navigate_to_report, download_report
    ).execute(
        output_dir=r"C:\Users\lu9887091\Downloads",
        filiais=["2", "4", "6"],
        start_date="01/03/2026",
        end_date="20/03/2026",
        login="DEFIS_AUX20",
        password="lfT#1020304050",
    )
