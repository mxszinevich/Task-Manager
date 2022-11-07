from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func

from db.models import Base


class Task(Base):
    __tablename__ = "tasks"

    name = Column(String(300), nullable=False)
    body = Column(String)
    created = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
