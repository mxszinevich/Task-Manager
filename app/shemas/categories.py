from shemas import OrmBaseModel


class BaseCategory(OrmBaseModel):
    name: str


class CategoryDetail(BaseCategory):
    id: int


class CategoryCreate(BaseCategory):
    ...
