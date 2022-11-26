from datetime import datetime

from config import settings


def datetime_formatting(value: datetime | None) -> str | None:
    if isinstance(value, datetime):
        return value.strftime(settings.app.dtime_out_f)
    return value
