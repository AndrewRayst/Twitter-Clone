import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from shared import TweetTestDataClass, TUsersTest
from src.tweets.models import TweetModel


@pytest.fixture(scope="module")
async def tweet_data(users: TUsersTest) -> TweetTestDataClass:
    """
    The fixture for getting tweet data
    :param users: user who added in database
    :return: tweet data
    """
    return TweetTestDataClass(users[0])


@pytest.fixture(scope="module")
async def tweet(users: TUsersTest, async_session: AsyncSession) -> TweetTestDataClass:
    """
    The fixture for adding tweet in database and getting tweet data
    :param users: user who added in database
    :param async_session: async session for connecting to database
    :return: tweet data
    """
    tweet = TweetTestDataClass(users[0])
    instance: TweetModel = tweet.get_instance()

    async_session.add(instance)
    await async_session.commit()

    tweet.id = instance.id

    return tweet
