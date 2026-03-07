import logging
import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config.settings import settings
from core.database.connection import run_migrations
from modules.automation.presentation.routes import livros_fiscais_routes
from modules.data_process.presentation.routes import periodo_routes

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


# Lifecycle events to setup the SQLite db before accepting traffic
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Iniciando %s v%s", settings.APP_NAME, settings.APP_VERSION)
    logger.info("Banco de dados: %s", settings.DATABASE_PATH)
    logger.info("Workspace: %s", settings.WORKSPACE_ROOT)

    await run_migrations()

    yield

    logger.info("Encerrando aplicação.")


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Backend local para apuração de ICMS.",
    lifespan=lifespan,
)

# CORS — permite requisições do Electron (localhost)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://localhost:*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
# app.include_router(automation.router)
app.include_router(periodo_routes.router, prefix="/api/v1")
app.include_router(livros_fiscais_routes.router, prefix="/api/v1")


@app.get("/health", tags=["Sistema"])
async def health_check():
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
