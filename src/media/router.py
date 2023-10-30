from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import JSONResponse
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.core import get_session
from src.exceptions import ExistError
from src.media.config import LOADING_IMAGE_SRC
from src.media.schemas import SuccessMediaResponseSchema
from src.media.service import add_image_media
from src.media.tasks import process_image
from src.utils import return_server_exception, return_user_exception

router: APIRouter = APIRouter(
    prefix="/api/medias",
    tags=["Media"],
)


@router.post("/", response_model=SuccessMediaResponseSchema, status_code=201)
async def _add_media(
    api_key: str,
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
) -> dict | JSONResponse:
    """
    The endpoint for adding media file
    :param api_key: API key of the user who wants to add image media.
    :param file: media file
    :return: id of media in database
    """
    try:
        logger.info("adding image to the database")
        await logger.complete()

        image_id: int = await add_image_media(
            session=session, api_key=api_key, image_src=LOADING_IMAGE_SRC
        )

        logger.info("creating process of the image")
        await logger.complete()

        process_image.delay(image_id=image_id, image_data=file.file.read())

        return {"result": True, "media_id": image_id}

    except ExistError as exc:
        return await return_user_exception(exception=exc)
    except Exception as exc:
        return await return_server_exception(exception=exc)
