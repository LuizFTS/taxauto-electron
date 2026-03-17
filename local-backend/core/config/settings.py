import os
import socket
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


def find_free_port(start=8000, end=8100):
    for port in range(start, end):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    raise RuntimeError("No free ports available")


class Settings(BaseSettings):

    APP_NAME: str = "TaxAuto"
    APP_VERSION: str = "0.1.0"
    HOST: str = "127.0.0.1"
    PORT: int = Field(default_factory=find_free_port)
    DEBUG: bool = False

    # Caminhos base derivados do sistema operacional do usuário
    USER_DOCUMENTS: Path = Path.home() / "Documents"
    APP_DATA: Path = Path(os.getenv("APPDATA", Path.home() / ".local/share")) / "taxauto"

    # Workspace do usuário
    WORKSPACE_ROOT: Path = USER_DOCUMENTS / "TaxAuto"

    # Storage interno da aplicação
    DATABASE_PATH: Path = APP_DATA / "database.db"
    LOGS_PATH: Path = APP_DATA / "logs"
    DATA_PATH: Path = APP_DATA / "data"

    # Subpastas de input esperadas por período
    INPUT_FOLDERS: list[str] = [
        "LIVRO_ENTRADA",
        "LIVRO_SAIDA",
        "DIFAL",
        "ST",
        "ESTORNO_CREDITO",
        "ESTORNO_MERCADORIA_DETERIORADA",
        "FOT",
        "FRETE_ENTRADA",
        "FRETE_SAIDA",
        "INEXIGIBILIDADE",
    ]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
