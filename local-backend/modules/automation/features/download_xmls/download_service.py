import logging
import math
import os
import re
import subprocess
import unicodedata
from pathlib import Path
from time import sleep, time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from modules.automation.infrastructure.selenium import SeleniumDriver

logger = logging.getLogger(__name__)


class DownloadService:
    def __init__(self, files_per_download: int = 500):
        self.files_per_download = files_per_download

    def _fill_input(self, d: SeleniumDriver, element_id: str, valor: str):
        logger.debug(f"Preenchendo campo '{element_id}' com valor '{valor}'")
        d.driver.execute_script(f"""
            var el = document.getElementById('{element_id}');
            el.value = '{valor}';

            el.dispatchEvent(new Event('input', {{ bubbles: true }}));
            el.dispatchEvent(new Event('change', {{ bubbles: true }}));

            el.dispatchEvent(new KeyboardEvent('keydown', {{
                key: 'Tab', code: 'Tab', keyCode: 9, which: 9, bubbles: true
            }}));
            el.dispatchEvent(new KeyboardEvent('keyup', {{
                key: 'Tab', code: 'Tab', keyCode: 9, which: 9, bubbles: true
            }}));

            el.blur();
        """)
        logger.debug(f"Campo '{element_id}' preenchido com sucesso")

    def _get_total_records(self, driver):
        texto = driver.find_element(
            By.CSS_SELECTOR, "#globalForm\\:mainTable_paginator_bottom .ui-paginator-current"
        ).text

        match = re.search(r"\(de\s+(\d+)\)", texto)

        if not match:
            logger.warning(f"Não foi possível extrair total de registros do texto: '{texto}'")
            return 0

        total = int(match.group(1))
        logger.debug(f"Total de registros encontrado: {total}")
        return total

    def _download(
        self,
        filial_str,
        start_date,
        end_date,
        tipo_documento,
        tp_operacao,
        output_dir,
        d,
        total_registros,
    ) -> str:
        # Seleciona todos via checkbox
        logger.debug(f"[Filial {filial_str}] Selecionando todos os registros via checkbox")
        checkbox_box = d.find_element(
            By.XPATH,
            "//input[@name='globalForm:mainTable_checkbox']/../../div[contains(@class,'ui-chkbox-box')]",
        )
        checkbox_box.click()

        # Extrai cookies e ViewState
        logger.debug(f"[Filial {filial_str}] Extraindo JSESSIONID e ViewState")
        jsessionid = ""
        for cookie in d.get_cookies():
            if cookie["name"] == "JSESSIONID":
                jsessionid = cookie["value"]
                break

        if not jsessionid:
            logger.warning(f"[Filial {filial_str}] JSESSIONID não encontrado nos cookies!")

        view_state = d.find_element(By.NAME, "javax.faces.ViewState").get_attribute("value")
        logger.debug(f"[Filial {filial_str}] ViewState extraído com sucesso")

        if total_registros == 1:
            file_path = os.path.join(output_dir, f"{filial_str}.xml")
        else:
            file_path = os.path.join(output_dir, f"{filial_str}.zip")
        logger.info(f"[Filial {filial_str}] Iniciando download via PowerShell → {file_path}")

        ps_script = f"""
        $session = New-Object Microsoft.PowerShell.Commands.WebRequestSession
        $session.Cookies.Add(
            (New-Object System.Net.Cookie("JSESSIONID", "{jsessionid}", "/", "100.126.64.15"))
        )

        $url = "http://100.126.64.15:8080/adged/notas-fiscais.xhtml"

        $body = @{{
            "globalForm" = "globalForm"
            "globalForm:filtroAvancado:dtPeriodoInicio_input" = "{start_date}"
            "globalForm:filtroAvancado:dtPeriodoFinal_input"  = "{end_date}"
            "globalForm:filtroAvancado_active" = "0"
            "globalForm:menuFiltros_input" = "{tp_operacao}"
            "globalForm:mainTable:tpFiltroValor" = "TODOS"
            "globalForm:mainTable:status:filter" = "autorizado"
            "globalForm:mainTable:tipoDoc:filter" = "{tipo_documento}"
            "globalForm:mainTable_selection" = ""
            "globalForm:btnDownload" = ""
            "javax.faces.ViewState" = "{view_state}"
        }}

        Invoke-WebRequest `
            -Uri $url `
            -Method POST `
            -WebSession $session `
            -Body $body `
            -ContentType "application/x-www-form-urlencoded" `
            -OutFile "{file_path}"
        """

        try:
            result = subprocess.run(
                ["powershell", "-Command", ps_script], capture_output=True, text=True
            )

            if result.returncode != 0:
                logger.error(
                    f"[Filial {filial_str}] PowerShell retornou erro (code {result.returncode}): {result.stderr.strip()}"
                )
                raise Exception(f"PowerShell falhou com código {result.returncode}")

            checkbox_box.click()

            if not os.path.exists(file_path):
                logger.error(f"[Filial {filial_str}] Arquivo não foi criado em: {file_path}")
                raise Exception("Arquivo de download não encontrado após execução do PowerShell")

            file_size = os.path.getsize(file_path)
            logger.info(
                f"[Filial {filial_str}] Download concluído com sucesso → {file_path} ({file_size / 1024:.1f} KB)"
            )
            return file_path

        except Exception as e:
            logger.error(f"[Filial {filial_str}] Erro ao gerar relatório: {e}", exc_info=True)
            raise Exception(f"Erro ao gerar relatório da filial {filial_str}") from e

    def normalizar_texto(self, texto):
        texto = texto.strip().lower()
        texto = unicodedata.normalize("NFD", texto)
        return "".join(c for c in texto if unicodedata.category(c) != "Mn")

    def encontrar_option_por_tipo(self, driver, tipo):
        if tipo == 1:
            termo = "saida"
        elif tipo == 2:
            termo = "entrada"
        else:
            raise ValueError("tipo deve ser 1 ou 2")

        select_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="globalForm:menuFiltros_input"]'))
        )

        select_obj = Select(select_element)

        for i, option in enumerate(select_obj.options):
            texto_normalizado = self.normalizar_texto(option.text)

            if termo in texto_normalizado:
                return {"indice": i, "texto": option.text, "value": option.get_attribute("value")}

        return None

    def execute(
        self,
        driver: SeleniumDriver,
        output_dir: str,
        filial: int,
        start_date: str,
        end_date: str,
        tipo_documento: int,
        tipo_operacao: int,
        first_time: bool = False,
    ):
        filial_str = str(filial).zfill(2)
        logger.info(f"[Filial {filial_str}] Iniciando download do relatório")
        logger.debug(
            f"[Filial {filial_str}] Parâmetros: start_date={start_date}, end_date={end_date}, tipo_documento={tipo_documento}, tipo_operacao={tipo_operacao}"
        )

        s = driver
        d = s.driver

        # Preenchimento do período
        logger.info(
            f"[Filial {filial_str}] Preenchendo filtros de data: {start_date} até {end_date}"
        )
        self._fill_input(s, "globalForm:filtroAvancado:dtPeriodoInicio_input", start_date)
        self._fill_input(s, "globalForm:filtroAvancado:dtPeriodoFinal_input", end_date)

        logger.debug(f"[Filial {filial_str}] Clicando em pesquisar")
        s.clicar('//*[@id="globalForm:filtroAvancado:btnPesquisar"]')
        s.wait_overlay_status(d)

        # Filtro de operação
        logger.debug(f"[Filial {filial_str}] Selecionando tipo de operação: {tipo_operacao}")

        result = self.encontrar_option_por_tipo(d, tipo_operacao)

        if not result:
            raise ValueError(f"Não foi possível encontrar o tipo de operação {tipo_operacao}")

        tp_index = result["indice"] + 1
        tp_value = result["value"]

        s.clicar('//*[@id="globalForm:menuFiltros"]/div[2]/span')
        s.clicar(f'//*[@id="globalForm:menuFiltros_panel"]/div/ul/li[{str(tp_index)}]')
        sleep(5)
        s.wait_overlay_status(d)

        # Filtros de status e tipo de documento
        logger.debug(f"[Filial {filial_str}] Aplicando filtro de status: autorizado")
        s.selecionar('//*[@id="globalForm:mainTable:status:filter"]', "autorizado")
        sleep(5)
        s.wait_overlay_status(d)

        logger.debug(
            f"[Filial {filial_str}] Aplicando filtro de tipo de documento: {tipo_documento}"
        )
        s.selecionar('//*[@id="globalForm:mainTable:tipoDoc:filter"]', str(tipo_documento))
        s.wait_overlay_status(d)
        total_registros_antes = self._get_total_records(d)
        total_registros = total_registros_antes
        sleep(5)

        # Aguarda estabilização do total de registros
        logger.debug(
            f"[Filial {filial_str}] Total de registros antes dos filtros: {total_registros_antes}"
        )

        inicio = time()
        timeout = 120

        while True:
            total_registros = self._get_total_records(d)
            if (
                total_registros < total_registros_antes
                or time() - inicio > timeout
                or total_registros == 0
            ):
                logger.debug(f"[Filial {filial_str}] Registros estabilizaram em {total_registros}")
                break
            sleep(0.5)

        logger.info(f"[Filial {filial_str}] Total de registros após filtros: {total_registros}")

        if total_registros == 0:
            logger.warning(f"[Filial {filial_str}] Não há registros para baixar!")
            return []

        total_paginas = 1
        if total_registros > self.files_per_download:
            total_paginas = math.ceil(total_registros / self.files_per_download)
            logger.info(
                f"[Filial {filial_str}] Registros excedem {self.files_per_download} — total de páginas: {total_paginas}"
            )

        # Seleciona 100 por página
        logger.debug(
            f"[Filial {filial_str}] Configurando paginação para {self.files_per_download} registros por página"
        )
        s.wait_overlay_status(d)

        option = d.find_element(
            By.XPATH, '//*[@id="globalForm:mainTable_paginator_bottom"]/select/option[6]'
        )

        d.execute_script(
            """
            arguments[0].value = arguments[1];
        """,
            option,
            self.files_per_download,
        )

        s.selecionar(
            '//*[@id="globalForm:mainTable_paginator_bottom"]/select', f"{self.files_per_download}"
        )
        s.clicar("/html/body")

        while True:
            rows = d.find_elements(By.XPATH, '//*[@id="globalForm:mainTable_data"]/tr')
            quantidade_rows = len(rows)

            logger.debug(
                f"[Filial {filial_str}] Linhas carregadas: {quantidade_rows}/{total_registros}"
            )

            if quantidade_rows == self.files_per_download or quantidade_rows == total_registros:
                logger.info(f"[Filial {filial_str}] Todas as {total_registros} linhas carregadas")
                break

            sleep(3)

        paths = []

        parent_dir = os.path.join(output_dir, f"{filial_str}")
        parent_dir = Path(parent_dir)
        parent_dir.mkdir(exist_ok=True)

        if total_paginas == 1:
            parent_dir = os.path.join(parent_dir, f"{1}")
            parent_dir = Path(parent_dir)
            parent_dir.mkdir(exist_ok=True)

            path = self._download(
                filial_str,
                start_date,
                end_date,
                tipo_documento,
                tp_value,
                str(parent_dir),
                d,
                total_registros,
            )
            paths.append(path)
            return paths

        for i in range(total_paginas):
            parent_dir = os.path.join(parent_dir, f"{i+1}")
            parent_dir = Path(parent_dir)
            parent_dir.mkdir(exist_ok=True)
            print("i = ", i)
            if i == 12:
                print("12")

            if i != 0:
                nnf_before = d.find_element(
                    By.XPATH, '//*[@id="globalForm:mainTable_data"]/tr[1]/td[2]/div'
                ).text

                s.wait_overlay_status(d)
                # s.clicar(f'//*[@id="globalForm:mainTable_paginator_bottom"]/span[4]/span[{i + 1}]')
                s.clicar('//*[@id="globalForm:mainTable_paginator_bottom"]/span[5]/span')

                while True:
                    nnf_after = d.find_element(
                        By.XPATH, '//*[@id="globalForm:mainTable_data"]/tr[1]/td[2]/div'
                    ).text
                    print("nnf_after - ", nnf_after)

                    if nnf_after != nnf_before:
                        nnf_before = nnf_after
                        print("nnf_after - ", nnf_after)

                        break
                    print("nnf_before - ", nnf_before)
                    sleep(1)

            # tem que retornar um array de strings nesse caso
            path = self._download(
                filial_str,
                start_date,
                end_date,
                tipo_documento,
                tp_value,
                str(parent_dir),
                d,
                total_registros,
            )
            paths.append(path)
            parent_dir = os.path.join(output_dir, f"{filial_str}")

        return paths
