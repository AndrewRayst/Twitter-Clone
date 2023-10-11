from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import AccessError, ExistError
from src.tweets.models import TweetModel
from src.users.models import UserModel
from src.utils import get_hash


async def add_tweet(session: AsyncSession, api_key: str, tweet_content: str) -> int:
    """
    The service for adding tweet in database
    :param session: session to connect to the database.
    :param api_key: API key of the user who wants to add the tweet
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


async def delete_tweet(
    session: AsyncSession,
    tweet_id: int,
    api_key: str,
) -> None:
    """
    The service for adding tweet in database
    :param session: session to connect to the database.
    :param api_key: API key of the user who wants to delete the tweet
    :param tweet_id: ID of the tweet
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

    # Getting the tweet by id
    tweet_query: Select = select(TweetModel).where(TweetModel.id == tweet_id)
    tweet: TweetModel = await session.scalar(tweet_query)

    # Checking the existence of a tweet
    if not tweet:
        raise ExistError("The tweet doesn't exist")

    # Checking whether the user has the right to delete a tweet
    if tweet.user_id != user.id:
        raise AccessError("User can't delete this tweet.")

    # Deleting tweet in database
    await session.delete(tweet)
    await session.commit()