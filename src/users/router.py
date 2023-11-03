from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from loguru import logger
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.core import get_session
from src.exceptions import ConflictError, ExistError
from src.schemas import SuccessResponseSchema
from src.users.models import UserModel
from src.users.schemas import SuccessResponseUserSchema
from src.users.service import (
    check_and_get_user_by_api_key,
    follow_user,
    get_me,
    get_user,
    unfollow_user,
)
from src.utils import (
    api_key_param,
    return_custom_exception,
    return_server_exception,
    return_user_exception,
)

router: APIRouter = APIRouter(
    prefix="/api/users",
    tags=["Users"],
)


@router.get("/me", response_model=SuccessResponseUserSchema, status_code=200)
async def _get_my_profile(
    api_key: str = Depends(api_key_param), session: AsyncSession = Depends(get_session)
) -> dict | JSONResponse:
    """
    The endpoint for retrieving your own profile
    :param api_key: user api key who wants to retrieve the profile
    :return: the user profile
    """
    try:
        logger.info("getting the user own profile")
        await logger.complete()
        return {
            "result": True,
            "user": await get_me(session=session, api_key=api_key),
        }
    except ExistError as exc:
        return await return_user_exception(exception=exc)
    except Exception as exc:
        return await return_server_exception(exception=exc)


@router.get("/{user_id}", response_model=SuccessResponseUserSchema, status_code=200)
async def _get_user_profile(
    user_id: int,
    api_key: str = Depends(api_key_param),
    session: AsyncSession = Depends(get_session),
) -> dict | JSONResponse:
    """
    The endpoint for retrieving the user profile
    :param user_id: id of the user whose profile you want to get
    :param api_key: user api key who wants to retrieve the profile
    :return: the user profile
    """
    try:
        logger.info("getting the user who wants to retrieve the profile")
        await logger.complete()
        await check_and_get_user_by_api_key(
            api_key=api_key,
            session=session,
            error_message="The user who wants to retrieve the profile doesn't exist",
        )

        logger.info("getting the user profile by another user")
        await logger.complete()
        return {
            "result": True,
            "user": await get_user(session=session, user_id=user_id),
        }
    except ExistError as exc:
        return await return_user_exception(exception=exc)
    except Exception as exc:
        return await return_server_exception(exception=exc)


@router.post("/{user_id}/follow", response_model=SuccessResponseSchema, status_code=201)
async def _follow(
    user_id: int,
    api_key: str = Depends(api_key_param),
    session: AsyncSession = Depends(get_session),
) -> dict | JSONResponse:
    """
    The endpoint for following user
    :param user_id: id of the user to follow
    :param api_key: API key of the user who wants to follow
    """
    try:
        logger.info("getting the user who wants to follow")
        await logger.complete()
        follower: UserModel = await check_and_get_user_by_api_key(
            api_key=api_key,
            session=session,
            error_message="The follower doesn't exist",
        )

        logger.info("following one user by another")
        await logger.complete()
        await follow_user(session=session, user_id=user_id, follower=follower)

        return {"result": True}

    except (ExistError, ConflictError) as exc:
        return await return_user_exception(exception=exc)
    except IntegrityError as exc:
        return await return_custom_exception(
            exception=exc,
            message="Follower has already followed the user",
            error_type="ConflictError",
            status_code=409,
        )
    except Exception as exc:
        return await return_server_exception(exception=exc)


@router.delete(
    "/{user_id}/follow", response_model=SuccessResponseSchema, status_code=200
)
async def _unfollow(
    user_id: int,
    api_key: str = Depends(api_key_param),
    session: AsyncSession = Depends(get_session),
) -> dict | JSONResponse:
    """
    The endpoint for unfollowing user
    :param user_id: id of the user to unfollow
    :param api_key: API key of the user who wants to unfollow
    """
    try:
        logger.info("getting the user who wants to unfollow")
        await logger.complete()
        follower: UserModel = await check_and_get_user_by_api_key(
            api_key=api_key,
            session=session,
            error_message="The follower doesn't exist",
        )

        logger.info("unfollowing one user by another")
        await logger.complete()
        await unfollow_user(session=session, user_id=user_id, follower=follower)

        return {"result": True}

    except ExistError as exc:
        return await return_user_exception(exception=exc)
    except Exception as exc:
        return await return_server_exception(exception=exc)
