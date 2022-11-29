from db.repositories.base import SqlAlchemyRepo


class BaseTableRepository(SqlAlchemyRepo):
    @property
    def column(self):
        return self.model.c
