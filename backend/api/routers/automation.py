from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from infrastructure.database.local_db import get_db_session
from infrastructure.repositories.task_repository import TaskRepository
from domain.models.tasks import StartTaskRequest, AutomationResponse
from workers.executor import TaskExecutor
from usecases.process_task import SampleAutomationUseCase

router = APIRouter(prefix="/api/v1/automations", tags=["Automations"])

# Register available automations here
USE_CASE_REGISTRY = {
    "sample_task": SampleAutomationUseCase,
    # Add generic fiscal reporting use-cases here
}

executor = TaskExecutor(use_case_registry=USE_CASE_REGISTRY)

async def get_task_repo(session: AsyncSession = Depends(get_db_session)):
    return TaskRepository(session)

@router.post("/start")
async def start_automation(
    request: StartTaskRequest, 
    background_tasks: BackgroundTasks,
    repo: TaskRepository = Depends(get_task_repo)
):
    if request.task_name not in USE_CASE_REGISTRY:
        raise HTTPException(status_code=400, detail="Invalid task_name")
        
    job_id = str(uuid.uuid4())
    
    # Create the task record securely
    await repo.create_task(job_id, request.task_name, request.payload)
    
    # We must not block the REST endpoint for potentially long operations
    background_tasks.add_task(
        executor.run_task_in_background,
        job_id=job_id,
        task_name=request.task_name,
        payload=request.payload,
        task_repo=repo
    )
    
    return {"status": "accepted", "job_id": job_id}

@router.get("/{job_id}")
async def get_automation_status(
    job_id: str,
    repo: TaskRepository = Depends(get_task_repo)
):
    record = await repo.get_task(job_id)
    if not record:
        raise HTTPException(status_code=404, detail="Task not found")
        
    return {
        "status": record.status,
        "job_id": record.id,
        "name": record.name,
        "result_data": record.result
    }
