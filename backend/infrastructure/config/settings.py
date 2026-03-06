import os
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "ICMS Apurador"
    APP_VERSION: str = "0.1.0"
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    DEBUG: bool = True

    # Caminhos base derivados do sistema operacional do usuário
    USER_DOCUMENTS: Path = Path.home() / "Documents"
    APP_DATA: Path = Path(os.getenv("APPDATA", Path.home() / ".local/share")) / "icms_apurador"

    # Workspace do usuário
    WORKSPACE_ROOT: Path = USER_DOCUMENTS / "Apuracao_ICMS"

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