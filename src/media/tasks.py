import io
from asyncio import current_task, get_event_loop
from contextlib import asynccontextmanager
from typing import AnyStr, AsyncGenerator

import PIL
from loguru import logger
from PIL import Image
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session

from src.celery import celery
from src.database.core import session_maker
from src.media.service import update_image_src
from src.utils import get_random_string

loop = get_event_loop()


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


async def update_image_src_in_database_async(image_id: int, image_src: str) -> None:
    async with scoped_session() as session:
        await update_image_src(image_id=image_id, image_src=image_src, session=session)


@celery.task
def process_image(
    image_id: int,
    image_data: AnyStr,
) -> None:
    # loading an image data to PIL Image
    image = Image.open(io.BytesIO(image_data))  # type: ignore

    # changing an image size
    image.thumbnail((600, 600), resample=PIL.Image.LANCZOS)

    # preparing to save an image
    thumb_file = io.BytesIO()
    save_args = {"format": image.format, "progressive": True}

    if image.format == "JPEG":
        save_args["quality"] = 85

    # saving an image
    image.save(thumb_file, **save_args)

    # running the task for sending image to storage
    send_image_to_storage.delay(
        image_id=image_id,
        image_data=image_data,
    )
    logger.info("process_image")


@celery.task
def send_image_to_storage(
    image_id: int,
    image_data: AnyStr,
) -> None:
    # sending image to storage and getting src
    image_src = get_random_string()

    # running task for updating image source in database
    update_image_src_in_database.delay(
        image_id=image_id,
        image_src=image_src,
    )
    logger.info("send_image_to_storage")


@celery.task
def update_image_src_in_database(
    image_id: int,
    image_src: str,
) -> None:
    # running async loop
    loop.run_until_complete(
        update_image_src_in_database_async(image_id=image_id, image_src=image_src)
    )
    logger.info("update_image_src_in_database")
