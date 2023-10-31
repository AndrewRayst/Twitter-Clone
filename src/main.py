from datetime import datetime

import sentry_sdk
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from loguru import logger
from prometheus_fastapi_instrumentator import Instrumentator
from redis import asyncio as aioredis

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


sentry_sdk.init(
    dsn=config.SENTRY_DNS,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
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


metrics_instrument = Instrumentator().instrument(application)


@application.on_event("startup")
async def startup() -> None:
    metrics_instrument.expose(application)

    redis_url = config.REDIS_URL_TEST if config.TESTING else config.REDIS_URL
    redis = aioredis.from_url(redis_url, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


@application.on_event("shutdown")
async def _on_shutdown() -> None:
    await shutdown_db()
