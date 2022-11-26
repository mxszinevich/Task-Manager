from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from db.constants import StatusType
from db.models import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    is_superuser = Column(Boolean, nullable=False, default=False)
    created = Column(DateTime, server_default=func.now())

    tasks = relationship("Task", backref="user")

    @property
    def count_task_created(self) -> int:
        return len([task for task in self.tasks if task.status == StatusType.CREATED])

    @property
    def count_task_completed(self) -> int:
        return len([task for task in self.tasks if task.status == StatusType.COMPLETED])

    @property
    def count_task_expired(self) -> int:
        return len([task for task in self.tasks if task.status == StatusType.EXPIRED])
