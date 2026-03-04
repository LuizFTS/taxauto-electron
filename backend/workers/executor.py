import logging
from typing import Dict, Any, Type
from usecases.process_task import BaseUseCase
from domain.errors import TaskNotFoundError

logger = logging.getLogger("executor")

class TaskExecutor:
    """
    Executes tasks in the background and updates their state via a repository.
    In a real app, you can enhance this with thread pools or separate process workers.
    """
    def __init__(self, use_case_registry: Dict[str, Type[BaseUseCase]]):
        self.registry = use_case_registry

    async def run_task_in_background(
        self, 
        job_id: str, 
        task_name: str, 
        payload: Dict[str, Any],
        task_repo # Injected task repository
    ):
        try:
            logger.info(f"job_id={job_id} task_name={task_name} status=started")
            use_case_class = self.registry.get(task_name)
            
            if not use_case_class:
                logger.error(f"job_id={job_id} error=unknown_task")
                await task_repo.update_status(job_id, "failed", {"error": "Unknown task type"})
                return

            use_case = use_case_class() # Initialize with dependencies if needed
            
            # Execute business logic
            result = await use_case.execute(payload)
            
            # Update success state
            await task_repo.update_status(job_id, "completed", result)
            logger.info(f"job_id={job_id} task_name={task_name} status=completed")
            
        except Exception as e:
            logger.exception(f"job_id={job_id} task_name={task_name} status=failed err={str(e)}")
            await task_repo.update_status(job_id, "failed", {"error": str(e)})
