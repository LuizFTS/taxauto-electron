from fastapi import FastAPI, Depends
import uvicorn
import asyncio
from contextlib import asynccontextmanager

from api.routers import automation
from api.dependencies.auth import verify_token
from infrastructure.database.local_db import engine
from infrastructure.database.init_db import init_models
import sys

# Lifecycle events to setup the SQLite db before accepting traffic
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing Database...")
    await init_models(engine)
    print("Database Initialized.")
    yield
    print("Shutting down Application...")
    # Add cleanup resources if needed (browser closing, etc)
    
app = FastAPI(title="TaxAuto Python Automation Backend", lifespan=lifespan)

# Mount Routers - Globally protected by auth token verification
app.include_router(
    automation.router, 
    dependencies=[Depends(verify_token)]
)

@app.get("/health", tags=["System"])
async def health_check():
    """
    Called by Electron to check if the backend is ready
    """
    return {"status": "healthy"}

if __name__ == "__main__":
    # Electron passes --port dynamically, or fallback to dev port
    port = 8000
    if "--port" in sys.argv:
        try:
            port_index = sys.argv.index("--port") + 1
            port = int(sys.argv[port_index])
        except (ValueError, IndexError):
            pass

    uvicorn.run("main:app", host="127.0.0.1", port=port, reload=False)
