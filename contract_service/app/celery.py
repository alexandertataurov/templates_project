from celery import Celery
import os

CELERY_BROKER = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")

celery_app = Celery("tasks", broker=CELERY_BROKER)


@celery_app.task
def add(x, y):
    return x + y
