# infrastructure/utils/selenium_driver.py
import os
import shutil
import subprocess
import time
from time import sleep
from typing import Callable

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


class SeleniumDriver:
    """
    Wrapper para WebDriver do Selenium, encapsulando ações comuns
    como clicar, digitar, selecionar, aguardar elementos e captchas.
    """

    def __init__(
        self, path: str, error_handler: Callable[[Exception], None] = None, headless: bool = True
    ):
        """
        :param driver: instância de Selenium WebDriver
        :param error_handler: função callback para tratamento de erro (opcional)
        """
        self.error_handler = error_handler or (lambda e: print(f"Erro Selenium: {e}"))

        self.path = path
        self.chrome_options = Options()
        self.prefs = {
            "download.default_directory": self.path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True,
            "safebrowsing.enabled": True,
            "safebrowsing.disable_download_protection": True,
            "profile.default_content_setting_values.automatic_downloads": 1,
            "exceptions.insecure_download_allowed": {
                "http://100.126.64.15:8080": {"last_modified": "1", "setting": 1},
            },
        }
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.chrome_options.add_experimental_option("prefs", self.prefs)
        self.chrome_options.add_argument("--ignore-certificate-errors")
        self.chrome_options.add_argument("--safebrowsing-disable-download-protection")

        if headless:
            self.chrome_options.add_argument("--headless=new")
            self.chrome_options.add_argument("--disable-gpu")
            self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--start_maximized")
        self.driver = webdriver.Chrome(options=self.chrome_options)

    # ==========================
    # Ações básicas
    # ==========================
    def clicar(self, path):
        # Verifica se overlay está presente e visível

        overlays = self.driver.find_elements(By.CSS_SELECTOR, "div.ui-widget-overlay")
        for overlay in overlays:
            if overlay.is_displayed():
                self.driver
                # instead of raise an exception, delete overlay component
                self.driver.execute_script("arguments[0].remove();", overlay)
                # raise Exception("Overlay detectado, clique bloqueado!")

        # Se não houver overlay, tenta clicar normalmente
        element = self._waitTillClickable(path)
        try:
            element.click()
        except Exception as e:
            # se por algum motivo outro elemento ainda interceptar
            print("Message: ", e)
            raise Exception(f"Outro elemento bloqueou o clique: {str(e)}")

    def clicar_any_paths(self, paths: list[str]):
        # Verifica se overlay está presente e visível
        overlays = self.driver.find_elements(By.CSS_SELECTOR, "div.ui-widget-overlay")
        for overlay in overlays:
            if overlay.is_displayed():
                self.driver
                raise Exception("Overlay detectado, clique bloqueado!")

        # Se não houver overlay, tenta clicar normalmente em qualquer um dos caminhos fornecidos
        for path in paths:
            try:

                element = self._waitTillClickable(path, timeout=5)

                if element:
                    element.click()
                    return path
            except Exception as e:
                print(f"Não conseguiu clicar no caminho {path}: {e}")
                continue

    def digitar(self, path, text):
        element = self._waitTillClickable(path)
        element.send_keys(text)

    def digitar_blur(self, path, text):
        element = self._waitTillClickable(path)
        element.send_keys(text)
        element.send_keys(Keys.TAB)

    def get_element(self, path):
        element = self._waitTillClickable(path)
        return element

    def press_tab(self, element):
        element.send_keys(Keys.TAB)

    def digitar_por_elemento(self, element, text):
        element.send_keys(text)

    def selecionar(self, path, option, timeout=30):
        element = self._waitTillClickable(path, timeout)
        select = Select(element)
        select.select_by_value(option)

    def aguardar(self, path, timeout=10):

        WebDriverWait(self.driver, timeout).until(lambda d: d.find_element(By.XPATH, path))

    def elemento_no_iframe(self, iframe_xpath, elemento_xpath):
        try:
            # Localiza o iframe e troca de contexto
            iframe = self.driver.find_element(By.XPATH, iframe_xpath)
            self.driver.switch_to.frame(iframe)

            # Localiza o elemento dentro do iframe
            elemento = self.driver.find_element(By.XPATH, elemento_xpath)

            # Volta para o contexto principal
            self.driver.switch_to.default_content()

            return elemento
        except Exception as e:
            print("Erro: Message - ", e)
            self.driver.switch_to.default_content()
            return None

    def click_js(self, path: str):
        element = self.driver.find_element(By.XPATH, path)
        self.driver.execute_script("arguments[0].click();", element)

    def aguardar_captcha(self, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[name="captcha"][vc-recaptcha]'))
        )
        iframe = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'div[name="captcha"][vc-recaptcha] iframe')
            )
        )
        self.driver.switch_to.frame(iframe)

        checkbox = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((By.ID, "recaptcha-anchor"))
        )
        checkbox.click()

        WebDriverWait(self.driver, 300).until(
            lambda d: d.find_element(By.ID, "recaptcha-anchor").get_attribute("aria-checked")
            == "true"
        )

        self.driver.switch_to.default_content()

    def clear(self, path):
        element = self._waitTillClickable(path)
        element.clear()

    def _waitTillClickable(self, path, timeout=30):
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, path)))
            return element
        except Exception as e:
            print("Message ", e)
            raise Exception("Erro ao encontrar elemento clicável.")

    ## Browser Manager

    def get_driver(self):
        return self.driver

    def quit(self):
        self.driver.quit()

    def esperar_download(self, caminho):
        while True:

            # Se o arquivo final existe e não tem extensão .crdownload (download em andamento)
            if os.path.exists(caminho):
                # print("Download concluído!")
                break

    def is_pdf_file(self, path: str) -> bool:
        try:
            with open(path, "rb") as f:
                return f.read(4) == b"%PDF"
        except Exception:
            return False

    def compare_files_before_and_after_download_pdf_file(
        self, path_name: str, file_name: str, timeout=60
    ) -> bool:
        inicio = time.time()

        # LOOP ATÉ TER MAIS ARQUIVOS QUE ANTES
        while True:
            if time.time() - inicio > timeout:
                print("Timeout aguardando novo arquivo.")
                return False

            files_after = set(os.listdir(path_name))

            if len(files_after) > len(self.files_before):
                new_ones = files_after - self.files_before
                # Ignora arquivos temporários do Chrome (.crdownload)

                validated_new_ones = []

                for f in new_ones:
                    if f.lower().endswith(".crdownload"):
                        continue

                    full_path = os.path.join(path_name, f)

                    if self.is_pdf_file(full_path):
                        validated_new_ones.append(f)

                if len(validated_new_ones) == 1:
                    new_file = validated_new_ones[0]
                    old_path = os.path.join(path_name, new_file)

                    base_name, _ = os.path.splitext(file_name)
                    new_path = os.path.join(path_name, base_name + ".pdf")

                    return self._move_file_waiting(old_path, new_path)

                elif len(validated_new_ones) > 1:
                    print("Mais de um arquivo PDF novo encontrado.")
                    subprocess.Popen(f'explorer "{path_name}"')
                    return True

            sleep(1)

    def _move_file_waiting(self, old_path, new_path, timeout=90):
        inicio = time.time()
        last_size = -1
        stable_count = 0

        while True:
            try:
                current_size = os.path.getsize(old_path)

                if current_size == last_size:
                    stable_count += 1
                else:
                    stable_count = 0

                last_size = current_size

                if stable_count >= 2:

                    with open(old_path, "rb"):
                        pass

                    shutil.move(old_path, new_path)
                    return True

            except (PermissionError, FileNotFoundError, OSError):
                pass

            if time.time() - inicio > timeout:
                print("Não foi possível mover o arquivo, ainda está sendo usado")
                return False

            sleep(0.5)
