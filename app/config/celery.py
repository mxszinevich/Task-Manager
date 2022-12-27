from celery import Celery
from celery.schedules import crontab

from .settings import settings

app = Celery(broker=settings.redis.dsn, include=["worker"])

app.conf.beat_schedule = {
    # tasks
    "task_status_update": {
        "task": "worker.task.task_update_status",
        "schedule": crontab(minute="*/1"),
    },
}
