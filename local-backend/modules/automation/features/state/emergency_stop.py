import logging

import keyboard

from modules.automation.features.state.automation_state import AutomationState

logger = logging.getLogger(__name__)


def setup_emergency_stop(state: AutomationState):
    def stop():
        logger.info("[SYSTEM] ESC pressed — stopping automation...")
        state.request_stop()

    keyboard.add_hotkey("esc", stop)
