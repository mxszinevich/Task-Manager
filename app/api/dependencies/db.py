from db import async_session_builder
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db_session():
    async_session: AsyncSession = async_session_builder()

    async with async_session() as session:
        yield session
        await session.commit()
