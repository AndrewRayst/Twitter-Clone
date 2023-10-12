from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from loguru import logger
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.core import get_session
from src.exceptions import AccessError, ExistError, ConflictError
from src.media.service import update_tweet_id
from src.schemas import SuccessResponseSchema
from src.tweets.schemas import SuccessTweetResponseSchema, TweetSchema
from src.tweets.service import add_tweet, delete_tweet, like_tweet, unlike_tweet

router: APIRouter = APIRouter(prefix="/api/tweets", tags=["Tweets"])


@router.post("/", response_model=SuccessTweetResponseSchema, status_code=201)
async def _add_tweet(
    tweet_json: TweetSchema,
    api_key: str,
    session: AsyncSession = Depends(get_session),
) -> dict | JSONResponse:
    """
    The endpoint for adding the tweet
    :param tweet_json: the data for adding the tweet
    :param api_key: API key of the user who wants to add the tweet
    :return: id of tweet in database
    """
    try:
        tweet_id: int = await add_tweet(
            session=session, api_key=api_key, tweet_content=tweet_json.tweet_data
        )

        if tweet_json.tweet_media_ids:
            await update_tweet_id(
                session=session, tweet_id=tweet_id, media_ids=tweet_json.tweet_media_ids
            )

        return {"result": True, "tweet_id": tweet_id}
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


@router.delete("/{tweet_id}", response_model=SuccessResponseSchema, status_code=200)
async def _delete_tweet(
    tweet_id: int,
    api_key: str,
    session: AsyncSession = Depends(get_session),
) -> dict | JSONResponse:
    """
    The endpoint for deleting the tweet by id
    :param tweet_id: tweet ID
    :param api_key: API key of the user who wants to delete the tweet
    """
    try:
        await delete_tweet(session=session, tweet_id=tweet_id, api_key=api_key)

        return {"result": True}
    except (ExistError, AccessError) as exc:
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


@router.post("/{tweet_id}/likes", response_model=SuccessResponseSchema, status_code=201)
async def _like_tweet(
    tweet_id: int, api_key: str, session: AsyncSession = Depends(get_session)
) -> dict | JSONResponse:
    """
    The endpoint for liking the tweet by id.
    :param tweet_id: id of the tweet to like
    :param api_key: API key of the user who wants to like the tweet
    """
    try:
        await like_tweet(session=session, tweet_id=tweet_id, api_key=api_key)
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
        logger.info("User has already liked the tweet")
        await logger.complete()
        return JSONResponse(
            status_code=409,
            content={
                "result": False,
                "error_type": "ConflictError",
                "error_message": "User has already liked the tweet",
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


@router.delete("/{tweet_id}/likes", response_model=SuccessResponseSchema, status_code=200)
async def _unlike_tweet(
    tweet_id: int, api_key: str, session: AsyncSession = Depends(get_session)
) -> dict | JSONResponse:
    """
    The endpoint for unliking the tweet by id.
    :param tweet_id: id of the tweet to unlike
    :param api_key: API key of the user who wants to unlike the tweet
    """
    try:
        await unlike_tweet(session=session, tweet_id=tweet_id, api_key=api_key)
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
        await logger.complete()
        return JSONResponse(
            status_code=400,
            content={
                "result": False,
                "error_type": "Exception",
                "error_message": "Oops, something went wrong :(\nTry again please",
            },
        )

