from datetime import datetime

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from loguru import logger

from src import config
from src.database.core import shutdown_db
from src.media.router import router as media_router
from src.tweets.router import router as tweets_router
from src.users.router import router as users_router

logger.add(
    f"../logs/{datetime.now().strftime('%Y-%m-%d')}_log.json",
    level="INFO",
    format="{level} {time} {message}",
    serialize=True,
    rotation="00:00",
    compression="zip",
)


application: FastAPI = FastAPI(
    debug=config.DEBUG,
    title="Twitter clone",
    version="0.1.0",
    description="Thesis by Andrey Telitsin for Skillbox",
)

application.mount(
    "/static",
    StaticFiles(directory=config.STATIC_FILES_PATH),
    name="static",
)


application.include_router(users_router)
application.include_router(media_router)
application.include_router(tweets_router)


@application.on_event("shutdown")
async def _on_shutdown() -> None:
    await shutdown_db()
