import logging
import subprocess

logger = logging.getLogger(__name__)


def cleanup_chromedriver():
    try:
        subprocess.run(
            ["taskkill", "/F", "/IM", "chromedriver.exe"],
            capture_output=True,
            check=False,
        )
        logger.info("[Helper] Chromedrivers finalizados")
    except Exception as e:
        logger.error("[Helper] Erro ao finalizar o chromedriver")
        logger.error(e)
