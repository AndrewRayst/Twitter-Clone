from datetime import datetime

from fastapi import FastAPI
from loguru import logger

import config
from database.core import shutdown_db

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


@application.on_event("shutdown")
async def _on_shutdown() -> None:
    await shutdown_db()
