from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from modules.automation.utils.selenium_driver import SeleniumDriver


class BrowserSession:
    def __init__(self, driver: SeleniumDriver):
        self.driver = driver

    def execute(self, login: str, password: str):
        self.driver.driver.get("http://100.126.64.15:8080/adged/login.xhtml")
        self._login(login, password)

    def _login(self, login: str, password: str):
        d = self.driver
        d.digitar('//*[@id="formLogin:usuario"]', login)
        d.digitar('//*[@id="formLogin:senha"]', password)
        d.clicar('//*[@id="formLogin:btnLogar"]')
        wait = WebDriverWait(d.driver, 10)

        wait.until(EC.element_to_be_clickable((By.ID, "formLogin:empresa_label")))
