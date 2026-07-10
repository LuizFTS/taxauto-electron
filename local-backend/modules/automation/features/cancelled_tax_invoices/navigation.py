import logging
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from modules.automation.infrastructure.selenium import SeleniumDriver

logger = logging.getLogger(__name__)


class Navigation:
    def execute(self, d: SeleniumDriver, filial: int):
        d.driver.get("http://100.126.64.15:8080/adged/login.xhtml")
        wait = WebDriverWait(d.driver, 360)

        # Open menu
        menu_trigger = wait.until(EC.element_to_be_clickable((By.ID, "formLogin:empresa_label")))
        sleep(2)
        menu_trigger.click()

        # Wait for panel to appear
        panel = wait.until(EC.visibility_of_element_located((By.ID, "formLogin:empresa_panel")))

        filial_str = str(int(filial)).zfill(2)

        lista_itens = panel.find_elements(By.CLASS_NAME, "ui-selectonemenu-item")
        encontrou = False

        for item in lista_itens:
            texto_item = item.text.strip()
            # Verifica se o número da filial está no texto (mais seguro que string exata)
            if f"FILIAL {filial_str}" in texto_item:
                item.click()
                encontrou = True
                # Espera o dropdown fechar
                wait.until(EC.invisibility_of_element_located((By.ID, "formLogin:empresa_panel")))
                break

        if not encontrou:
            logger.warning(f"Filial {filial_str} não encontrada na lista!")
            raise Exception(f"Filial {filial_str} não encontrada na lista!")

        # Clique no botão entrar (usando ID direto que é mais rápido que XPath)
        btn_entrar = wait.until(EC.element_to_be_clickable((By.ID, "formLogin:btnEntrar")))

        try:
            sleep(2)
            btn_entrar.click()
        except Exception:
            # Se ainda assim der erro de interceptação, usa JS
            d.driver.execute_script("arguments[0].click();", btn_entrar)

        wait.until(
            EC.visibility_of_element_located((By.ID, "globalForm:filtroAvancado:btnPesquisar"))
        )
