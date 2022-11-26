from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

from db.constants import StatusType
from db.models import Base, TaskCategory


class Task(Base):
    __tablename__ = "tasks"

    name = Column(String(300), nullable=False)
    body = Column(String)
    created = Column(DateTime, server_default=func.now())
    status = Column(ChoiceType(StatusType, impl=Integer()), default=StatusType.CREATED)
    completion_date = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    categories = relationship("Category", secondary=TaskCategory, backref="tasks")
