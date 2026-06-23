import logging
import math
import os
import re
import subprocess
import time
from time import sleep

from selenium.webdriver.common.by import By

from modules.automation.infrastructure.selenium import SeleniumDriver

logger = logging.getLogger(__name__)


class DownloadService:
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
        tp_operacao = "634" if tipo_operacao == 1 else "635"

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
        logger.debug(f"[Filial {filial_str}] Selecionando tipo de operação: {tp_operacao}")
        s.clicar('//*[@id="globalForm:menuFiltros"]/div[2]/span')
        s.clicar(f'//*[@id="globalForm:menuFiltros_panel"]/div/ul/li[{str(tipo_operacao)}]')
        sleep(5)

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
        sleep(5)

        # Aguarda estabilização do total de registros
        total_registros_antes = self._get_total_records(d)
        total_registros = total_registros_antes
        logger.debug(
            f"[Filial {filial_str}] Total de registros antes dos filtros: {total_registros_antes}"
        )

        inicio = time.time()
        timeout = 20
        logger.debug(
            f"[Filial {filial_str}] Aguardando estabilização dos registros (timeout: {timeout}s)"
        )
        while time.time() - inicio < timeout:
            total_registros = self._get_total_records(d)
            if total_registros < total_registros_antes:
                logger.debug(f"[Filial {filial_str}] Registros estabilizaram em {total_registros}")
                break
            sleep(0.5)
        else:
            logger.warning(
                f"[Filial {filial_str}] Timeout aguardando estabilização — usando total atual: {total_registros}"
            )

        logger.info(f"[Filial {filial_str}] Total de registros após filtros: {total_registros}")

        if total_registros > 1000:
            total_paginas = math.ceil(total_registros / 1000)
            logger.info(
                f"[Filial {filial_str}] Registros excedem 1000 — total de páginas: {total_paginas}"
            )

        # Seleciona 1000 por página
        logger.debug(f"[Filial {filial_str}] Configurando paginação para 1000 registros por página")
        s.wait_overlay_status(d)
        s.selecionar('//*[@id="globalForm:mainTable_paginator_bottom"]/select', "1000")
        s.clicar("/html/body")

        # Aguarda todas as linhas carregarem
        inicio = time.time()
        timeout = 360
        logger.debug(
            f"[Filial {filial_str}] Aguardando carregamento das linhas (timeout: {timeout}s)"
        )

        while True:
            rows = d.find_elements(By.XPATH, '//*[@id="globalForm:mainTable_data"]/tr')
            quantidade_rows = len(rows)

            logger.debug(
                f"[Filial {filial_str}] Linhas carregadas: {quantidade_rows}/{total_registros}"
            )

            if quantidade_rows == total_registros:
                logger.info(f"[Filial {filial_str}] Todas as {total_registros} linhas carregadas")
                break

            if time.time() - inicio > timeout:
                raise Exception(
                    f"[Filial {filial_str}] Timeout ao aguardar linhas — encontradas {quantidade_rows} de {total_registros}"
                )

            sleep(1)

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
