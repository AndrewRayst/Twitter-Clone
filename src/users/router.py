from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from loguru import logger
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.core import get_session
from src.exceptions import ConflictError, ExistError
from src.schemas import SuccessResponseSchema
from src.users.service import follow_user, unfollow_user

router: APIRouter = APIRouter(
    prefix="/api/users",
    tags=["Users"],
)


@router.post("/{user_id}/follow", response_model=SuccessResponseSchema, status_code=201)
async def _follow(
    user_id: int, api_key: str, session: AsyncSession = Depends(get_session)
) -> dict | JSONResponse:
    """
    The endpoint for following user
    :param user_id: id of the user to follow
    :param api_key: API key of the user who wants to follow
    """
    try:
        await follow_user(session, user_id, api_key)
        return {
            "result": True,
        }
    except (ExistError, ConflictError) as exc:
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
    except IntegrityError:
        logger.info("Follower has already followed the user")
        await logger.complete()
        return JSONResponse(
            status_code=409,
            content={
                "result": False,
                "error_type": "ConflictError",
                "error_message": "Follower has already followed the user",
            },
        )
    except Exception as exc:
        logger.warning(f"string representation: {exc.__str__()}, args: {str(exc.args)}")
        await logger.complete()
        return JSONResponse(
            status_code=400,
            content={
                "result": False,
                "error_type": "Exception",
                "error_message": "Oops, something went wrong :(\nTry again please",
            },
        )


@router.post(
    "/{user_id}/unfollow", response_model=SuccessResponseSchema, status_code=200
)
async def _unfollow(
    user_id: int, api_key: str, session: AsyncSession = Depends(get_session)
) -> dict | JSONResponse:
    """
    The endpoint for following user
    :param user_id: id of the user to follow
    :param api_key: API key of the user who wants to follow
    """
    try:
        await unfollow_user(session, user_id, api_key)
        return {
            "result": True,
        }
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
