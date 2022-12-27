import asyncio

from sqlalchemy.orm import sessionmaker

from config import app, settings
from db.repositories.tasks import TasksRepository
from db.session import AsyncSessionBuilder


@app.task
def task_update_status():
    async def task_():
        session_maker: sessionmaker = AsyncSessionBuilder(database_url=settings.db.dsn, echo=True)
        Session: sessionmaker = session_maker()
        async with Session() as session:
            task_repo = TasksRepository(session=session)
            await task_repo.tasks_changing_status()

    asyncio.run(task_())
