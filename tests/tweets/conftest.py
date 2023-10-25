import pytest
from sqlalchemy import Update, update
from sqlalchemy.ext.asyncio import AsyncSession

from shared import TweetTestDataClass, TUsersTest
from src.media.models import MediaModel
from src.tweets.models import TweetModel


@pytest.fixture(scope="function")
async def tweet_data(users: TUsersTest) -> TweetTestDataClass:
    """
    The fixture for getting tweet data
    :param users: user who added in database
    :return: tweet data
    """
    return TweetTestDataClass(users[0])


@pytest.fixture(scope="module")
async def tweet(
    users: TUsersTest,
    image_ids: list[int],
    async_session: AsyncSession
) -> TweetTestDataClass:
    """
    The fixture for adding tweet in database and getting tweet data
    :param users: user who added in database
    :param image_ids: image IDs for tweet
    :param async_session: async session for connecting to database
    :return: tweet data
    """
    tweet = TweetTestDataClass(users[0])
    instance: TweetModel = tweet.get_instance()

    async_session.add(instance)
    await async_session.flush()

    tweet.id = instance.id

    statement: Update = (
        update(MediaModel)
        .where(MediaModel.id.in_(image_ids))
        .values(tweet_id=tweet.id)
    )
    await async_session.execute(statement)

    await async_session.commit()

    return tweet
