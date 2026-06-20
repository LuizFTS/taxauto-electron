from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from modules.automation.infrastructure.selenium import SeleniumDriver


class BrowserSession:
    def execute(self, d: SeleniumDriver, login: str, password: str):
        d.driver.get("http://100.126.64.15:8080/adged/login.xhtml")
        self._login(d, login, password)

    def _login(self, d: SeleniumDriver, login: str, password: str):
        d.digitar('//*[@id="formLogin:usuario"]', login)
        d.digitar('//*[@id="formLogin:senha"]', password)
        d.clicar('//*[@id="formLogin:btnLogar"]')
        wait = WebDriverWait(d.driver, 10)

        wait.until(EC.element_to_be_clickable((By.ID, "formLogin:empresa_label")))
