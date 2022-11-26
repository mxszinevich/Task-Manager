from sqlalchemy import Column, ForeignKey, Integer, Table

from db.models import Base

TaskCategory = Table(
    "tasks_categories",
    Base.metadata,
    Column("task_id", Integer, ForeignKey("tasks.id", ondelete="CASCADE")),
    Column("category_id", Integer, ForeignKey("categories.id", ondelete="CASCADE")),
)
