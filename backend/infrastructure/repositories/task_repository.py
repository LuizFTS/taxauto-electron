# We use SQLAlchemy for repository implementation with async Support
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Column, String, JSON, select
from typing import Optional, Dict, Any
from infrastructure.database.local_db import Base

class TaskRecord(Base):
    __tablename__ = "tasks"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    status = Column(String, index=True)
    payload = Column(JSON, nullable=True)
    result = Column(JSON, nullable=True)

class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def create_task(self, task_id: str, name: str, payload: Dict[str, Any]) -> TaskRecord:
        record = TaskRecord(id=task_id, name=name, status="pending", payload=payload)
        self.session.add(record)
        await self.session.commit()
        return record
        
    async def get_task(self, task_id: str) -> Optional[TaskRecord]:
        result = await self.session.execute(select(TaskRecord).where(TaskRecord.id == task_id))
        return result.scalar_one_or_none()
        
    async def update_status(self, task_id: str, status: str, result_data: Optional[Dict[str, Any]] = None):
        record = await self.get_task(task_id)
        if record:
            record.status = status
            if result_data is not None:
                record.result = result_data
            await self.session.commit()
