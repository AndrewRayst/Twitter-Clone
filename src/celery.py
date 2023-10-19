from celery import Celery
from src import config

task_imports: list[str] = ["src.media.tasks"]

celery = Celery(
    "tasks",
    include=task_imports,
    broker=config.REDIS_URL,
)
