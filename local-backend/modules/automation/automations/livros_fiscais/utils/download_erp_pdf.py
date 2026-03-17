import logging
import re
import time
from pathlib import Path

import requests
from pywinauto import Desktop
from pywinauto.keyboard import send_keys

# ==========================
# CONFIG
# ==========================

BASE_URL = "https://portalweb.casadoadubo.com.br/reports/rwservlet/getjobid"
SERVER_PARAM = "?SERVER=Rep_Server_portalweb"

DOWNLOAD_DIR = Path(r"C:\Reports")
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

TIMEOUT_SECONDS = 30
POLL_INTERVAL = 0.5

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

# ==========================
# WINDOW HELPERS
# ==========================


def list_chrome_windows():
    return [
        w for w in Desktop(backend="uia").windows() if w.window_text().endswith(" - Google Chrome")
    ]


def cleanup_existing_report_tabs():
    logging.info("Checking for existing report tabs...")

    for window in list_chrome_windows():
        title = window.window_text()
        if "getjobid" in title:
            logging.info(f"Closing stale report tab: {title}")
            window.set_focus()
            time.sleep(0.3)
            send_keys("^w")
            time.sleep(0.5)

    logging.info("Cleanup completed")


def find_report_window():
    for window in list_chrome_windows():
        title = window.window_text()
        if "getjobid" in title:
            return window
    return None


def wait_for_report(timeout=TIMEOUT_SECONDS):
    logging.info("Waiting for new Chrome report tab...")
    start = time.time()

    while time.time() - start < timeout:
        window = find_report_window()
        if window:
            logging.info(f"Detected new report tab: {window.window_text()}")
            return window
        time.sleep(POLL_INTERVAL)

    raise TimeoutError("Report window not detected")


# ==========================
# DOWNLOAD
# ==========================


def extract_jobid_from_title(title: str):
    match = re.search(r"getjobid(\d+)", title)
    return match.group(1) if match else None


def download_pdf(jobid: str, output_path: str):
    url = f"{BASE_URL}{jobid}{SERVER_PARAM}"

    output_path = Path(output_path)

    if output_path.exists():
        logging.info(f"File already exists: {output_path}")
        return output_path

    logging.info(f"Downloading from {url}")

    response = requests.get(url, timeout=60)
    response.raise_for_status()

    if "application/pdf" not in response.headers.get("Content-Type", ""):
        raise ValueError("Endpoint did not return PDF")

    output_path.write_bytes(response.content)

    if output_path.stat().st_size == 0:
        raise ValueError("Downloaded file is empty")

    logging.info(f"Saved to {output_path}")
    return output_path


def close_tab(window):
    logging.info("Closing report tab...")
    window.set_focus()
    time.sleep(0.3)
    send_keys("^w")
    logging.info("Tab closed")


# ==========================
# MAIN
# ==========================


def download_erp_pdf(path_download: str):
    try:
        # Step 2 — Wait for new tab
        window = wait_for_report()

        title = window.window_text()
        jobid = extract_jobid_from_title(title)

        if not jobid:
            raise ValueError("Could not extract jobid from window title")

        # Step 3 — Download
        download_pdf(jobid, path_download)

        # Step 4 — Close new tab
        close_tab(window)

        logging.info("Automation completed successfully")
        return 0

    except Exception as e:
        logging.error(f"Automation failed: {e}")
        return 1
