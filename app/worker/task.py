from config.celery import app


@app.task
def task_update_status():
    ...
