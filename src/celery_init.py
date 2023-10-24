from celery import Celery

from src import config

TASK_IMPORTS: list[str] = ["src.media.tasks"]
REDIS_URL: str = config.REDIS_URL_TEST if config.TESTING else config.REDIS_URL

celery_app = Celery(
    "tasks",
    include=TASK_IMPORTS,
    broker=REDIS_URL,
)
