from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from modules.automation.utils.selenium_driver import SeleniumDriver


class NavigateToReport:
    def __init__(self, driver: SeleniumDriver):
        self.driver = driver

    def execute(self, filial: int):
        d = self.driver

        d.driver.get("http://100.126.64.15:8080/adged/login.xhtml")

        wait = WebDriverWait(d.driver, 10)

        menu_trigger = wait.until(EC.element_to_be_clickable((By.ID, "formLogin:empresa_label")))
        menu_trigger.click()

        # 2. Espera o painel com as opções aparecer
        panel = wait.until(EC.visibility_of_element_located((By.ID, "formLogin:empresa_panel")))

        if int(filial) < 70:
            # 3. Encontra a opção desejada e clica nela
            opcao_desejada = f"CASA DO ADUBO - FILIAL {str(filial).zfill(2)}"
        else:
            opcao_desejada = f"CASAL COMERCIO E SERVICOS - FILIAL {str(filial).zfill(2)}"
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
