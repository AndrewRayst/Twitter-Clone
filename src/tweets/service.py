from sqlalchemy import select, Select
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import ExistError
from src.users.models import UserModel
from src.tweets.models import TweetModel
from src.utils import get_hash


async def add_tweet(
        session: AsyncSession, api_key: str, tweet_content: str
) -> int:
    """
    The service for adding tweet in database
    :param session: session to connect to the database.
    :param api_key: API key of the user who wants to add image media.
    :param tweet_content: text of the tweet
    :return: id of the tweet in database
    """
    # Getting user
    user_query: Select = select(UserModel).where(
        UserModel.api_key_hash == get_hash(api_key)
    )
    user: UserModel = await session.scalar(user_query)

    # Checking the existence of a user
    if not user:
        raise ExistError("The user doesn't exist")

    # Adding tweet in database
    instance: TweetModel = TweetModel(user_id=user.id, content=tweet_content)

    session.add(instance)
    await session.commit()

    return instance.id
