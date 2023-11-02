import io
from asyncio import get_event_loop
from typing import AnyStr

import PIL
from botocore.client import BaseClient
from loguru import logger
from PIL import Image

from src import config
from src.celery_init import celery_app, scoped_session
from src.media import config as media_config
from src.media.service import update_image_src
from src.utils import get_unique_filename
from src.yandex_s3 import session as s3_session

loop = get_event_loop()


@celery_app.task
def load_image(image_id: int, image_data: AnyStr) -> None:
    """
    task for load image to the storage and update src in the database
    :param image_id: the image record id.
    :param image_data: data of the images
    :return: None
    """
    logger.info("optimizing image")
    # optimizing image
    image, filetype = process_image(image_data=image_data)

    logger.info("sending image to storage")
    # sending image to storage
    image_src: str = send_image_to_storage(
        filetype=filetype.lower(),
        image_data=image,
    )

    logger.info("updating image source in database")
    # updating image source in database
    update_image_src_in_database(
        image_id=image_id,
        image_src=image_src,
    )


def process_image(image_data: AnyStr) -> tuple[bytes, str]:
    """
    optimization images
    :param image_data: data of the image
    :return: optimized image data and image type
    """
    # loading an image data to PIL Image
    image = Image.open(io.BytesIO(image_data))  # type: ignore
    filetype: str = image.format

    # changing an image size
    image.thumbnail((600, 600), resample=PIL.Image.LANCZOS)

    # preparing to save an image
    thumb_file = io.BytesIO()
    save_args = {"format": filetype, "progressive": True}

    if image.format == "JPEG":
        save_args["quality"] = 85

    # saving an image
    image.save(thumb_file, **save_args)

    return thumb_file.getvalue(), filetype


def send_image_to_storage(image_data: AnyStr, filetype: str) -> str:
    """
    load image to yandex s3 storage
    :param image_data: data of the image.
    :param filetype: type of image.
    :return: the image src in storage
    """
    # sending image to storage and getting src
    if config.TESTING or config.DEBUG:
        return "image_src_test"

    s3_client: BaseClient = s3_session.client(
        service_name="s3", endpoint_url=config.YANDEX_S3_ENDPOINT
    )

    filename = get_unique_filename(filetype)

    response = s3_client.put_object(
        Bucket=media_config.YANDEX_S3_BUCKET_NAME,
        Key="images/" + filename,
        Body=image_data,
    )

    status_code: int = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
    if status_code != 200:
        logger.warning("image upload failed")

    return media_config.YANDEX_S3_IMAGES_URL + filename


def update_image_src_in_database(image_id: int, image_src: str) -> None:
    """
    update image src in the database.
    :param image_id: the image record id.
    :param image_src: new image src in storage
    :return: None
    """
    # running async loop
    loop.run_until_complete(
        update_image_src_in_database_async(image_id=image_id, image_src=image_src)
    )


async def update_image_src_in_database_async(image_id: int, image_src: str) -> None:
    """
    async update image src in the database.
    :param image_id: the image record id.
    :param image_src: new image src in storage
    :return: None
    """
    await logger.complete()

    async with scoped_session() as session:
        await update_image_src(image_id=image_id, image_src=image_src, session=session)
