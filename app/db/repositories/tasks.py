from typing import Type

from db.models import Task
from db.repositories.base import BaseRepository


class TasksRepository(BaseRepository):
    @property
    def model(self) -> Type[Task]:
        return Task
