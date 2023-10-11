from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.core import get_session
from src.exceptions import ExistError
from src.media.service import update_tweet_id
from src.tweets.schemas import SuccessTweetResponseSchema, TweetSchema
from src.tweets.service import add_tweet

router: APIRouter = APIRouter(
    prefix="/api/tweets",
    tags=["Tweets"]
)


@router.post("/", response_model=SuccessTweetResponseSchema, status_code=201)
async def _add_tweet(
    tweet_json: TweetSchema,
    api_key: str,
    session: AsyncSession = Depends(get_session),
) -> dict | JSONResponse:
    """
    The endpoint for adding the tweet
    :param tweet_json: the data for adding the tweet
    :param api_key: API key of the user who wants to follow
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
