from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.db import get_db_session


class SessionRepository:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self._session = session

    @property
    def session(self) -> AsyncSession:
        return self._session
