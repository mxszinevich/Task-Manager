from sqlalchemy import Boolean, Column, DateTime, String, func

from db.models import Base


class User(Base):
    __tablename__ = "users"

    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    is_superuser = Column(Boolean, nullable=False, default=False)
    created = Column(DateTime, server_default=func.now())
