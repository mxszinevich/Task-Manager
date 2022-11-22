from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from config import settings


class AsyncSessionBuilder:
    def __init__(self, database_url: str, echo=False):
        self.database_url = database_url
        self.engine = create_async_engine(database_url, echo=echo)

    def __call__(self, *args, **kwargs) -> AsyncSession:
        self.session = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)
        return self.session


async_session_builder = AsyncSessionBuilder(database_url=settings.db.dsn, echo=settings.db.echo)
