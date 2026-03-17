class DomainError(Exception):
    """Base class for domain errors."""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

class TaskNotFoundError(DomainError):
    def __init__(self, task_id: str):
        super().__init__(f"Task with ID {task_id} not found.")

class AutomationExecutionError(DomainError):
    def __init__(self, detail: str):
        super().__init__(f"Automation failed: {detail}")
