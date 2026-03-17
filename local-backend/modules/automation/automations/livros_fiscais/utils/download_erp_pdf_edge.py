import logging
import re
import time
import unicodedata
from pathlib import Path

import requests
from pywinauto import Desktop
from pywinauto.keyboard import send_keys

# ==========================
# CONFIG
# ==========================

BASE_URL = "https://portalweb.casadoadubo.com.br/reports/rwservlet/getjobid"
SERVER_PARAM = "?SERVER=Rep_Server_portalweb"
TIMEOUT_SECONDS = 30
POLL_INTERVAL = 0.5

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

# ==========================
# HELPERS
# ==========================


def normalize(text: str) -> str:
    """Remove zero-width spaces e outros caracteres invisíveis (categoria Unicode Cf)."""
    return "".join(c for c in text if unicodedata.category(c) != "Cf")


def list_edge_windows():
    return [
        w
        for w in Desktop(backend="uia").windows()
        if "Microsoft Edge" in normalize(w.window_text())
    ]


def _is_report_title(title: str) -> bool:
    """
    Cobre todas as variações conhecidas de título que o Edge gera
    ao abrir a URL do relatório:
      - getjobid12345 - Microsoft Edge
      - getjobid12345.pdf - Microsoft Edge
      - https://portalweb.../getjobid12345?... - Microsoft Edge
    """
    normalized = normalize(title).lower()
    return "getjobid" in normalized or "rwservlet" in normalized


def extract_jobid_from_title(title: str) -> str | None:
    match = re.search(r"getjobid(\d+)", normalize(title), re.IGNORECASE)
    return match.group(1) if match else None


# ==========================
# WINDOW HELPERS
# ==========================


def cleanup_existing_report_tabs_edge():
    logging.info("Checking for existing report tabs in Edge...")
    for window in list_edge_windows():
        title = window.window_text()
        if _is_report_title(title):
            logging.info(f"Closing stale tab: {normalize(title)!r}")
            try:
                window.set_focus()
                time.sleep(0.3)
                send_keys("^w")
                time.sleep(0.5)
            except Exception as e:
                logging.warning(f"Could not close window: {e}")
    logging.info("Cleanup completed")


def wait_for_report_edge(timeout=TIMEOUT_SECONDS):
    """
    Aguarda a aba do relatório aparecer no Edge.
    Estratégia dupla: detecta pelo título E monitora janelas novas,
    pois o Edge pode demorar para atualizar o título enquanto carrega o PDF.
    """
    logging.info("Waiting for Edge report tab...")
    start = time.time()

    known_titles = {normalize(w.window_text()) for w in list_edge_windows()}

    while time.time() - start < timeout:
        current_windows = list_edge_windows()

        for window in current_windows:
            title = window.window_text()
            clean_title = normalize(title)

            # Critério 1 — título já contém getjobid (carregamento completo)
            if _is_report_title(title):
                logging.info(f"Detected report tab by title: {clean_title!r}")
                return window

            # Critério 2 — janela nova apareceu (Edge ainda carregando o PDF)
            if clean_title not in known_titles and "Microsoft Edge" in clean_title:
                logging.info(f"New Edge window detected, waiting for title: {clean_title!r}")
                time.sleep(1.5)
                title = window.window_text()
                if _is_report_title(title):
                    logging.info(f"Title confirmed after wait: {normalize(title)!r}")
                    return window

        time.sleep(POLL_INTERVAL)

    raise TimeoutError(
        f"Edge report window not detected within {timeout}s. "
        "Verifique se o Edge está abrindo a URL do relatório corretamente."
    )


# ==========================
# DOWNLOAD
# ==========================


def download_pdf(jobid: str, output_path: str) -> Path:
    url = f"{BASE_URL}{jobid}{SERVER_PARAM}"
    output_path = Path(output_path)

    if output_path.exists():
        logging.info(f"File already exists: {output_path}")
        return output_path

    logging.info(f"Downloading from {url}")
    response = requests.get(url, timeout=60)
    response.raise_for_status()

    content_type = response.headers.get("Content-Type", "")
    if "application/pdf" not in content_type:
        raise ValueError(f"Expected PDF, got: {content_type}")

    output_path.write_bytes(response.content)

    if output_path.stat().st_size == 0:
        raise ValueError("Downloaded file is empty")

    logging.info(f"Saved to {output_path}")
    return output_path


def close_tab(window):
    logging.info("Closing Edge report tab...")
    try:
        window.set_focus()
        time.sleep(0.3)
        send_keys("^w")
        logging.info("Tab closed")
    except Exception as e:
        logging.error(f"Failed to close tab: {e}")


# ==========================
# MAIN
# ==========================


def download_erp_pdf_edge(path_download: str) -> int:
    try:
        window = wait_for_report_edge()

        title = window.window_text()
        jobid = extract_jobid_from_title(title)

        if not jobid:
            raise ValueError(
                f"Não foi possível extrair jobid do título: {normalize(title)!r}\n"
                "O Edge pode estar exibindo o título do PDF em vez da URL."
            )

        download_pdf(jobid, path_download)
        close_tab(window)

        logging.info("Edge automation completed successfully")
        return 0

    except Exception as e:
        logging.error(f"Edge automation failed: {e}")
        return 1
