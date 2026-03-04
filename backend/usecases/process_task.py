from typing import Any, Dict
from abc import ABC, abstractmethod

class BaseUseCase(ABC):
    @abstractmethod
    async def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        pass

class SampleAutomationUseCase(BaseUseCase):
    """
    Example concrete use case for processing a specific task like downloading a fiscal report.
    Dependencies (like browser services) would typically be injected here.
    """
    def __init__(self, browser_service=None):
        # We can inject services here
        from services.browser_automation import BrowserAutomationService
        self.browser_service = browser_service or BrowserAutomationService()
        
    async def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        # Orchestrating business logic
        url = payload.get("url", "https://default.com")
        result = await self.browser_service.run_flow(url, payload)
        
        # We can implement domain assertions here
        return {"status": "success", "data": result}
