import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Electron passing token
    PYTHON_BACKEND_TOKEN: str = os.getenv("PYTHON_BACKEND_TOKEN", "dev-token")
    
    # DB path
    DB_PATH: str = os.getenv("DB_PATH", "sqlite+aiosqlite:///./local_db.sqlite")

settings = Settings()
