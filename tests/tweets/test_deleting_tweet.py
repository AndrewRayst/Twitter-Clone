from typing import Sequence

from httpx import AsyncClient
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from shared import TweetTestDataClass
from src.media.models import MediaModel
from src.tweets.models import TweetModel


async def test_delete_tweet_without_user(
    tweet: TweetTestDataClass, async_client: AsyncClient
) -> None:
    """
    Test for deleting tweet without the user.
    :param async_client: client for requesting.
    :return: None
    """
    response = await async_client.delete(
        f"tweets/{tweet.id}",
    )

    assert response.status_code == 422


async def test_delete_tweet_without_existing_user(
    tweet: TweetTestDataClass, async_client: AsyncClient
) -> None:
    """
    Test for deleting tweet without the existing user.
    :param async_client: client for requesting.
    :return: None
    """
    response = await async_client.delete(
        f"tweets/{tweet.id}",
        headers={"Api-Key": ""},
    )

    assert response.status_code == 400

    response_data: dict = response.json()
    assert response_data.get("result") is False


async def test_delete_tweet_with_correct_data(
    tweet: TweetTestDataClass,
    async_session: AsyncSession,
    async_client: AsyncClient,
) -> None:
    """
    Test for deleting tweet with the correct data.
    :param async_client: client for requesting.
    :param async_session: session for async connecting to the database.
    :return: None
    """
    response = await async_client.delete(
        f"tweets/{tweet.id}",
        headers={"Api-Key": tweet.user.api_key},
    )

    assert response.status_code == 200

    response_data: dict = response.json()
    assert response_data.get("result") is True

    # getting tweet
    tweet_query: Select = (
        select(TweetModel)
        .where(TweetModel.id == tweet.id)
        .where(TweetModel.content == tweet.content)
        .where(TweetModel.user_id == tweet.user.id)
    )

    tweet_record: TweetModel = await async_session.scalar(tweet_query)

    # checking existence of the tweet
    assert tweet_record is None

    # getting media
    media_query: Select = (
        select(MediaModel)
        .where(MediaModel.tweet_id == tweet.id)
    )

    media_response = await async_session.scalars(media_query)
    media: Sequence[MediaModel] = media_response.fetchall()

    # checking existence of media
    assert len(media) == 0
