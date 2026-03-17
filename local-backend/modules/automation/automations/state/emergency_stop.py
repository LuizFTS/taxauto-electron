import keyboard

from modules.automation.automations.state.automation_state import AutomationState


def setup_emergency_stop(state: AutomationState):
    def stop():
        print("ESC pressed — stopping automation...")
        state.request_stop()

    keyboard.add_hotkey("esc", stop)
