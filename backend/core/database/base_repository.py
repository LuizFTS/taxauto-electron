from core.database.connection import session
from core.database.mapper import row_to_entity, rows_to_entities


class BaseRepository:

    async def fetch_one(self, query: str, params: tuple, entity):
        async with session() as conn:
            cursor = await conn.execute(query, params)
            row = await cursor.fetchone()

            return row_to_entity(row, entity)

    async def fetch_all(self, query: str, params: tuple, entity):
        async with session() as conn:
            cursor = await conn.execute(query, params)
            rows = await cursor.fetchall()

            return rows_to_entities(rows, entity)

    async def execute(self, query: str, params: tuple = ()):
        async with session() as conn:
            cursor = await conn.execute(query, params)
            await conn.commit()

            return cursor.lastrowid
