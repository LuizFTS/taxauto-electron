import logging

import nazm as a

logger = logging.getLogger(__name__)


class Navigation:
    def execute(self):
        logger.info("[NAVIGATION] Executing navigation to Livros Fiscais")
        # open ERP
        # login
        # navigate menu
        # open livros fiscais screen
        a.press("f9")
        a.type("OBFI0200", 0.001)
        a.press("enter")
