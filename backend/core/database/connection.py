import logging
from contextlib import asynccontextmanager

import aiosqlite

from core.config.settings import settings

logger = logging.getLogger(__name__)

# DDL de todas as tabelas do sistema
MIGRATIONS: list[str] = [
    """
    CREATE TABLE IF NOT EXISTS company (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo       TEXT NOT NULL UNIQUE,
        nome         TEXT NOT NULL,
        ativa        INTEGER NOT NULL DEFAULT 1,
        created_at   TEXT NOT NULL DEFAULT (datetime('now','localtime')),
        updated_at   TEXT NOT NULL DEFAULT (datetime('now','localtime'))
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS branch (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo       TEXT NOT NULL UNIQUE,
        nome         TEXT NOT NULL,
        uf           TEXT NOT NULL,
        cnpj         TEXT NOT NULL,
        ie           TEXT NOT NULL,
        company_id   INTEGER NOT NULL,
        ativa        INTEGER NOT NULL DEFAULT 1,
        created_at   TEXT NOT NULL DEFAULT (datetime('now','localtime')),
        updated_at   TEXT NOT NULL DEFAULT (datetime('now','localtime')),
        
        FOREIGN KEY (company_id) REFERENCES company(id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS branch_group (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo       TEXT NOT NULL UNIQUE,
        nome         TEXT NOT NULL,
        analista     TEXT,
        ativo        INTEGER NOT NULL DEFAULT 1,
        created_at   TEXT NOT NULL DEFAULT (datetime('now','localtime')),
        updated_at   TEXT NOT NULL DEFAULT (datetime('now','localtime'))
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS branch_group_item (
        id             INTEGER PRIMARY KEY AUTOINCREMENT,
        group_id       INTEGER NOT NULL,
        branch_id      INTEGER NOT NULL,

        UNIQUE(group_id, branch_id),

        FOREIGN KEY (group_id) REFERENCES branch_group(id),
        FOREIGN KEY (branch_id) REFERENCES branch(id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS period (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        ano          INTEGER NOT NULL,
        mes          INTEGER NOT NULL,
        status       TEXT NOT NULL DEFAULT 'CRIADO',
        created_at   TEXT NOT NULL DEFAULT (datetime('now','localtime')),
        updated_at   TEXT NOT NULL DEFAULT (datetime('now','localtime')),
        atualizado_em TEXT NOT NULL DEFAULT (datetime('now','localtime')),
        UNIQUE (ano, mes)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS importacao (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        periodo_id    INTEGER NOT NULL,
        tipo_arquivo  TEXT NOT NULL,
        nome_arquivo  TEXT NOT NULL,
        caminho_raw   TEXT NOT NULL,
        total_linhas  INTEGER,
        status        TEXT NOT NULL DEFAULT 'PENDENTE',
        importado_em  TEXT NOT NULL DEFAULT (datetime('now','localtime')),

        FOREIGN KEY (periodo_id) REFERENCES periodo(id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS calculo_log (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        periodo_id  INTEGER NOT NULL,
        filial_id   INTEGER,
        etapa       TEXT NOT NULL,
        mensagem    TEXT NOT NULL,
        nivel       TEXT NOT NULL DEFAULT 'INFO',
        created_at  TEXT NOT NULL DEFAULT (datetime('now','localtime')),
        updated_at  TEXT NOT NULL DEFAULT (datetime('now','localtime')),

        FOREIGN KEY (periodo_id) REFERENCES periodo(id),
        FOREIGN KEY (filial_id) REFERENCES filial(id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS parametro_fiscal (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        chave      TEXT NOT NULL UNIQUE,
        valor      TEXT NOT NULL,
        descricao  TEXT,
        created_at TEXT NOT NULL DEFAULT (datetime('now','localtime')),
        updated_at TEXT NOT NULL DEFAULT (datetime('now','localtime'))
    );
    """,
]


def get_connection() -> aiosqlite.Connection:
    """Retorna uma conexão com o banco. Usar com 'async with'."""
    return aiosqlite.connect(settings.DATABASE_PATH)


@asynccontextmanager
async def session():
    """
    Unified database session manager.
    Handles startup, PRAGMAs, and automatic closing.
    """
    async with get_connection() as conn:
        conn.row_factory = aiosqlite.Row
        # WAL mode is great for concurrent reads/writes in Electron apps
        await conn.execute("PRAGMA journal_mode=WAL;")
        await conn.execute("PRAGMA foreign_keys=ON;")
        yield conn
        # Connection closes automatically here


async def run_migrations() -> None:
    """Executa todas as migrations na inicialização da aplicação."""
    settings.APP_DATA.mkdir(parents=True, exist_ok=True)

    async with get_connection() as conn:

        conn.row_factory = aiosqlite.Row
        await conn.execute("PRAGMA journal_mode=WAL;")
        await conn.execute("PRAGMA foreign_keys=ON;")

        for sql in MIGRATIONS:
            await conn.execute(sql)
        await conn.commit()

    logger.info("Migrations executadas com sucesso. DB: %s", settings.DATABASE_PATH)
