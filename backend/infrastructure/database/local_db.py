from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

from config import settings

engine = create_async_engine(
    settings.DB_PATH, 
    echo=False, 
    connect_args={"check_same_thread": False} if "sqlite" in settings.DB_PATH else {}
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def get_db_session():
    async with AsyncSessionLocal() as session:
        yield session
