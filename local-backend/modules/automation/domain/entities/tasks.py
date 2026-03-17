from typing import Any, Dict, Optional

from pydantic import BaseModel

# Domain Models (Pydantic for validation and passing around)

class AutomationRequest(BaseModel):
    task_id: str
    target_url: str
    action_type: str
    parameters: Dict[str, Any]

class AutomationResponse(BaseModel):
    status: str
    message: str
    result_data: Optional[Dict[str, Any]] = None

class StartTaskRequest(BaseModel):
    task_name: str
    payload: Dict[str, Any]
