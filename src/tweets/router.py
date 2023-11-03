from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, RedirectResponse
from loguru import logger
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.core import get_session
from src.exceptions import AccessError, ConflictError, ExistError
from src.media.service import update_tweet_id
from src.schemas import SuccessResponseSchema
from src.tweets.models import TweetModel
from src.tweets.schemas import (
    SuccessTweetPostResponseSchema,
    SuccessTweetsResponseSchema,
    TweetSchema,
)
from src.tweets.service import (
    add_tweet,
    check_and_get_tweet,
    delete_tweet,
    get_tweets,
    like_tweet,
    unlike_tweet,
)
from src.users.models import UserModel
from src.users.service import check_and_get_user_by_api_key
from src.utils import (
    api_key_param,
    return_custom_exception,
    return_server_exception,
    return_user_exception,
)

router: APIRouter = APIRouter(prefix="/api/tweets", tags=["Tweets"])


@router.post("/", response_model=SuccessTweetPostResponseSchema, status_code=201)
async def _add_tweet(
    tweet_json: TweetSchema,
    api_key: str = Depends(api_key_param),
    session: AsyncSession = Depends(get_session),
) -> dict | JSONResponse:
    """
    The endpoint for adding the tweet
    :param tweet_json: the data for adding the tweet
    :param api_key: API key of the user who wants to add the tweet
    :return: id of tweet in database
    """
    try:
        logger.info("getting the user by api key")
        await logger.complete()
        user: UserModel = await check_and_get_user_by_api_key(
            api_key=api_key,
            session=session,
            error_message="The user who wants to add the tweet doesn't exist",
        )

        logger.info("adding the new tweet")
        await logger.complete()
        tweet_id: int = await add_tweet(
            session=session, user=user, tweet_content=tweet_json.tweet_data
        )

        if tweet_json.tweet_media_ids:
            logger.info("updating tweet_id for linked media")
            await logger.complete()
            await update_tweet_id(
                session=session,
                tweet_id=tweet_id,
                user=user,
                media_ids=tweet_json.tweet_media_ids,
            )

        return {"result": True, "tweet_id": tweet_id}
    except ExistError as exc:
        return await return_user_exception(exception=exc)
    except Exception as exc:
        return await return_server_exception(exception=exc)


@router.delete("/{tweet_id}", response_model=SuccessResponseSchema, status_code=200)
async def _delete_tweet(
    tweet_id: int,
    api_key: str = Depends(api_key_param),
    session: AsyncSession = Depends(get_session),
) -> dict | JSONResponse:
    """
    The endpoint for deleting the tweet by id
    :param tweet_id: tweet ID
    :param api_key: API key of the user who wants to delete the tweet
    """
    try:
        logger.info("getting the user by api key")
        await logger.complete()
        user: UserModel = await check_and_get_user_by_api_key(
            api_key=api_key,
            session=session,
            error_message="The user who wants to delete the tweet doesn't exist",
        )

        await delete_tweet(session=session, tweet_id=tweet_id, user=user)

        return {"result": True}
    except (ExistError, AccessError) as exc:
        return await return_user_exception(exception=exc)
    except Exception as exc:
        return await return_server_exception(exception=exc)


@router.get("/", response_model=SuccessTweetsResponseSchema, status_code=200)
async def _get_tweets(
    limit: int | None = None,
    offset: int | None = None,
    api_key: str = Depends(api_key_param),
    session: AsyncSession = Depends(get_session),
) -> dict | JSONResponse:
    """
    The endpoint for getting tweets
    :param limit: limit of getting tweets
    :param offset: offset before getting tweets
    :param api_key: API key of the user who wants to add the tweet
    :return: id of tweet in database
    """
    try:
        # Checking limit and offset
        if type(limit) is int and limit <= 0:
            raise ValueError("the limit must be greater than 0.")
        elif type(limit) is int and limit > 20:
            raise ValueError("the limit must be equal to or less than 20.")

        if type(offset) is int and offset <= 0:
            raise ValueError("the offset must be greater than 0.")

        logger.info("getting tweets")
        await logger.complete()
        tweets = await get_tweets(
            session=session, api_key=api_key, limit=limit, offset=offset
        )

        return {"result": True, "tweets": tweets}

    except ExistError as exc:
        return await return_user_exception(exception=exc)
    except ValueError as exc:
        return await return_custom_exception(
            exception=exc,
            message=exc.__str__(),
            error_type="ValueError",
        )
    except Exception as exc:
        return await return_server_exception(exception=exc)


@router.post("/{tweet_id}/likes", response_model=SuccessResponseSchema, status_code=201)
async def _like_tweet(
    tweet_id: int,
    api_key: str = Depends(api_key_param),
    session: AsyncSession = Depends(get_session),
) -> dict | JSONResponse:
    """
    The endpoint for liking the tweet by id.
    :param tweet_id: id of the tweet to like
    :param api_key: API key of the user who wants to like the tweet
    """
    try:
        logger.info("getting user by api key")
        await logger.complete()
        user: UserModel = await check_and_get_user_by_api_key(
            session=session, api_key=api_key
        )

        logger.info("getting tweet by id")
        await logger.complete()
        tweet: TweetModel = await check_and_get_tweet(
            session=session, tweet_id=tweet_id
        )

        logger.info("liking tweet")
        await logger.complete()
        await like_tweet(session=session, tweet=tweet, user=user)

        return {"result": True}

    except (ExistError, ConflictError) as exc:
        return await return_user_exception(exception=exc)
    except IntegrityError as exc:
        return await return_custom_exception(
            exception=exc,
            message="User has already liked the tweet",
            error_type="ConflictError",
            status_code=409,
        )
    except Exception as exc:
        return await return_server_exception(exception=exc)


@router.delete(
    "/{tweet_id}/likes", response_model=SuccessResponseSchema, status_code=200
)
async def _unlike_tweet(
    tweet_id: int,
    api_key: str = Depends(api_key_param),
    session: AsyncSession = Depends(get_session),
) -> dict | JSONResponse:
    """
    The endpoint for unliking the tweet by id.
    :param tweet_id: id of the tweet to unlike
    :param api_key: API key of the user who wants to unlike the tweet
    """
    try:
        logger.info("getting user by api key")
        await logger.complete()
        user: UserModel = await check_and_get_user_by_api_key(
            session=session, api_key=api_key
        )

        logger.info("getting tweet by id")
        await logger.complete()
        tweet: TweetModel = await check_and_get_tweet(
            session=session, tweet_id=tweet_id
        )

        logger.info("unliking tweet")
        await logger.complete()
        await unlike_tweet(session=session, tweet=tweet, user=user)

        return {"result": True}
    except ExistError as exc:
        return await return_user_exception(exception=exc)
    except Exception as exc:
        return await return_server_exception(exception=exc)


@router.delete("/{user_id}/follow")
async def _unfollow(user_id: int) -> RedirectResponse:
    """
    The endpoint for redirecting to the right endpoint for unfollowing user.
    :param user_id: id of the user to unfollow
    :return: redirect
    """
    return RedirectResponse(f"/api/users/{user_id}/follow")
