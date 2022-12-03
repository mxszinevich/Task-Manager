from typing import Any

from sqlalchemy.sql.elements import BinaryExpression


class SqlHelperMixin:
    def build_filters(self, filter_params: dict[str, Any]) -> list[BinaryExpression]:
        return [getattr(self.model, filter_name) == filter_value for filter_name, filter_value in filter_params.items()]
