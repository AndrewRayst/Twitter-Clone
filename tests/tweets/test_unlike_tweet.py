from httpx import AsyncClient
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.tweets.models import TweetLikeModel
from tests.shared import TUsersTest, TweetTestDataClass


async def test_unlike_with_wrong_user(
    async_client: AsyncClient, liked_tweet: TweetTestDataClass
) -> None:
    """
    Test for checking endpoint for unlike the tweet with wrong user api key.
    :param async_client: client for requesting.
    :param liked_tweet: generated tweet with like
    :return: None
    """
    response = await async_client.delete(
        f"tweets/{liked_tweet.id}/likes",
        headers={
            "Api-Key": ""
        }
    )

    assert response.status_code == 400
    assert response.json().get("result") is False


async def test_unlike_without_user(
    async_client: AsyncClient, liked_tweet: TweetTestDataClass
) -> None:
    """
    Test for checking endpoint for unlike the tweet without user api key.
    :param async_client: client for requesting.
    :param liked_tweet: generated tweet with like
    :return: None
    """
    response = await async_client.delete(f"tweets/{liked_tweet.id}/likes")
    assert response.status_code == 422


async def test_unlike_with_wrong_tweet_id(
    async_client: AsyncClient, users: TUsersTest
) -> None:
    """
    Test for checking endpoint for unlike the tweet with wrong tweet id.
    :param async_client: client for requesting.
    :param users: generated users
    :return: None
    """
    response = await async_client.delete(
        "tweets/0/likes",
        headers={
            "Api-Key": users[0].api_key
        }
    )

    assert response.status_code == 400
    assert response.json().get("result") is False


async def test_unlike_with_correct_data(
    async_client: AsyncClient,
    async_session: AsyncSession,
    liked_tweet: TweetTestDataClass,
    users: TUsersTest,
) -> None:
    """
    Test for checking endpoint for unlike the tweet with correct data.
    :param async_client: client for requesting.
    :param async_session: session for async connecting to the database.
    :param liked_tweet: generated tweet with like
    :param users: generated users
    :return: None
    """
    response = await async_client.delete(
        f"tweets/{liked_tweet.id}/likes",
        headers={
            "Api-Key": users[0].api_key
        }
    )

    assert response.status_code == 200
    assert response.json().get("result") is True

    # getting like record
    query: Select = (
        select(TweetLikeModel)
        .where(TweetLikeModel.tweet_id == liked_tweet.id)
        .where(TweetLikeModel.user_id == users[0].id)
    )
    like_record: TweetLikeModel = await async_session.scalar(query)
    assert like_record is None
