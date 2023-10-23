from celery import Celery

from src import config

task_imports: list[str] = ["src.media.tasks"]

celery_app = Celery(
    "tasks",
    include=task_imports,
    broker=config.REDIS_URL_TEST if config.TESTING else config.REDIS_URL,
)
