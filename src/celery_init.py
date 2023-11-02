from asyncio import current_task
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from celery import Celery
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session

from src import config
from src.database.core import session_maker

TASK_IMPORTS: list[str] = ["src.media.tasks"]
REDIS_URL: str = config.REDIS_URL_TEST if config.TESTING else config.REDIS_URL

celery_app = Celery(
    "tasks",
    include=TASK_IMPORTS,
    broker=REDIS_URL,
    backend=REDIS_URL,
)


@asynccontextmanager
async def scoped_session() -> AsyncGenerator[AsyncSession, None]:
    scoped_factory = async_scoped_session(
        session_maker,
        scopefunc=current_task,
    )
    try:
        async with scoped_factory() as session:
            yield session
    finally:
        await scoped_factory.remove()
