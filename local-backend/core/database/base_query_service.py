from core.database.connection import session


class BaseQueryService:

    async def fetch_one(self, query: str, params: tuple = ()):
        async with session() as conn:
            cursor = await conn.execute(query, params)
            return await cursor.fetchone()

    async def fetch_all(self, query: str, params: tuple = ()):
        async with session() as conn:
            cursor = await conn.execute(query, params)
            return await cursor.fetchall()
