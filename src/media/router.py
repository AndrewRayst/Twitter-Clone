from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import JSONResponse
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.core import get_session
from src.exceptions import ExistError
from src.media.config import LOADING_IMAGE_SRC
from src.media.schemas import SuccessMediaResponseSchema
from src.media.service import add_image_media

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
    try:
        image_id: int = await add_image_media(
            session=session, api_key=api_key, image_src=LOADING_IMAGE_SRC
        )
        return {"result": True, "media_id": image_id}
    except ExistError as exc:
        logger.info(f"error name: {exc.get_name()}, error message: {exc.get_message()}")
        await logger.complete()
        return JSONResponse(
            status_code=400,
            content={
                "result": False,
                "error_type": exc.get_name(),
                "error_message": exc.get_message(),
            },
        )
    except Exception as exc:
        logger.warning(f"string representation: {exc.__str__()}, args: {str(exc.args)}")
        return JSONResponse(
            status_code=400,
            content={
                "result": False,
                "error_type": "Exception",
                "error_message": "Oops, something went wrong :(\nTry again please",
            },
        )
