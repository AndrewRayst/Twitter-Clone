import pytest

from shared import TweetTestDataClass, TUsersTest
from tests.conftest import session_maker
from src.tweets.models import TweetModel


@pytest.fixture(scope="module")
async def tweet(users: TUsersTest) -> TweetTestDataClass:
    tweet = TweetTestDataClass(user_id=users[0].id)
    instance = TweetModel(**tweet.__dict__())

    async with session_maker() as session:
        session.add(instance)
        await session.commit()

        tweet.id = instance.id

    return tweet
