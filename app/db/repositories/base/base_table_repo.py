from sqlalchemy.sql.base import ImmutableColumnCollection

from db.repositories.base import SqlAlchemyRepo


class BaseTableRepository(SqlAlchemyRepo):
    @property
    def column(self) -> ImmutableColumnCollection:
        return self.model.c
