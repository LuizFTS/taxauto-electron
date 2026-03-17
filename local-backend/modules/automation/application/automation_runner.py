from modules.automation.automations.state.automation_state import AutomationStoppedException


class AutomationRunner:

    def __init__(self, state):
        self.state = state

    def run(self, func, *args, **kwargs):

        self.state.reset()

        try:
            return func(*args, **kwargs)

        except AutomationStoppedException:
            raise
