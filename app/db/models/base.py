from sqlalchemy import Column, Integer
from sqlalchemy.orm import as_declarative


@as_declarative()
class Base:
    id = Column(Integer, primary_key=True)

    __mapper_args__ = {"eager_defaults": True}
