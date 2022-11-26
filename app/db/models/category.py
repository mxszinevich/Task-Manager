from sqlalchemy import Column, String

from db.models import Base


class Category(Base):
    __tablename__ = "categories"

    name = Column(String(250), nullable=False, unique=True)
