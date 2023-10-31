from httpx import AsyncClient
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.tweets.models import TweetLikeModel
from tests.shared import TUsersTest, TweetTestDataClass


async def test_like_with_wrong_user(
    async_client: AsyncClient, tweet: TweetTestDataClass
) -> None:
    """
    Test for checking endpoint for like the tweet with wrong user api key.
    :param async_client: client for requesting.
    :param tweet: generated tweet
    :return: None
    """
    response = await async_client.post(
        f"tweets/{tweet.id}/likes",
        params={
            "api_key": ""
        }
    )

    assert response.status_code == 400
    assert response.json().get("result") is False


async def test_like_without_user(
    async_client: AsyncClient, tweet: TweetTestDataClass
) -> None:
    """
    Test for checking endpoint for like the tweet without the user api key.
    :param async_client: client for requesting.
    :param tweet: generated tweet
    :return: None
    """
    response = await async_client.post(f"tweets/{tweet.id}/likes")
    assert response.status_code == 422


async def test_like_with_wrong_tweet_id(
    async_client: AsyncClient, users: TUsersTest
) -> None:
    """
    Test for checking endpoint for like the tweet with wrong tweet id.
    :param async_client: client for requesting.
    :param users: generated users
    :return: None
    """
    response = await async_client.post(
        "tweets/0/likes",
        params={
            "api_key": users[0].api_key
        }
    )

    assert response.status_code == 400
    assert response.json().get("result") is False


async def test_like_with_correct_data(
    async_client: AsyncClient,
    async_session: AsyncSession,
    tweet: TweetTestDataClass,
    users: TUsersTest,
) -> None:
    """
    Test for checking endpoint for like the tweet with correct data.
    :param async_client: client for requesting.
    :param async_session: session for async connecting to the database.
    :param tweet: generated tweet
    :param users: generated users
    :return: None
    """
    response = await async_client.post(
        f"tweets/{tweet.id}/likes",
        params={
            "api_key": users[0].api_key
        }
    )

    assert response.status_code == 201
    assert response.json().get("result") is True

    # getting like record
    query: Select = (
        select(TweetLikeModel)
        .where(TweetLikeModel.tweet_id == tweet.id)
        .where(TweetLikeModel.user_id == users[0].id)
    )
    like_record: TweetLikeModel = await async_session.scalar(query)
    assert like_record is not None


async def test_like_twice(
    async_client: AsyncClient,
    async_session: AsyncSession,
    tweet: TweetTestDataClass,
    users: TUsersTest,
) -> None:
    """
    Test for checking endpoint for like the tweet with correct data twice.
    :param async_client: client for requesting.
    :param async_session: session for async connecting to the database.
    :param tweet: generated tweet
    :param users: generated users
    :return: None
    """
    response = await async_client.post(
        f"tweets/{tweet.id}/likes",
        params={
            "api_key": users[0].api_key
        }
    )

    assert response.status_code == 409
    assert response.json().get("result") is False

    # getting like record
    query: Select = (
        select(TweetLikeModel)
        .where(TweetLikeModel.tweet_id == tweet.id)
        .where(TweetLikeModel.user_id == users[0].id)
    )
    like_record: TweetLikeModel = await async_session.scalar(query)
    assert like_record is not None
