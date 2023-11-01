from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import JSONResponse
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.core import get_session
from src.exceptions import ExistError
from src.media.config import LOADING_IMAGE_SRC
from src.media.schemas import SuccessMediaResponseSchema
from src.media.service import add_image_media
from src.media.tasks import load_image
from src.users.models import UserModel
from src.users.service import check_and_get_user_by_api_key
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
        logger.info("getting the user by api key")
        await logger.complete()
        user: UserModel = await check_and_get_user_by_api_key(
            api_key=api_key,
            session=session,
            error_message="The user who wants to add image media doesn't exist",
        )

        logger.info("adding image to the database")
        await logger.complete()
        image_id: int = await add_image_media(
            session=session, user=user, image_src=LOADING_IMAGE_SRC
        )

        logger.info("creating the process of the image")
        await logger.complete()
        load_image.delay(image_id=image_id, image_data=file.file.read())

        return {"result": True, "media_id": image_id}

    except ExistError as exc:
        return await return_user_exception(exception=exc)
    except Exception as exc:
        return await return_server_exception(exception=exc)
