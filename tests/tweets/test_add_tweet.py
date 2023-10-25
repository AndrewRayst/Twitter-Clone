from typing import Sequence

from httpx import AsyncClient
from sqlalchemy import select, Select
from sqlalchemy.ext.asyncio import AsyncSession

from shared import TweetTestDataClass
from src.media.models import MediaModel
from src.tweets.models import TweetModel


async def test_add_tweet_without_user(
        tweet_data: TweetTestDataClass,
        image_ids: list[int],
        async_session: AsyncSession,
        async_client: AsyncClient
) -> None:
    response = await async_client.post(
        "tweets/",
        json={
            "tweet_data": tweet_data.content,
            "tweet_media_ids": image_ids,
        }
    )

    assert response.status_code == 422


async def test_add_tweet_without_existing_user(
        tweet_data: TweetTestDataClass,
        image_ids: list[int],
        async_session: AsyncSession,
        async_client: AsyncClient
) -> None:
    response = await async_client.post(
        "tweets/",
        params={"api_key": ""},
        json={
            "tweet_data": tweet_data.content,
            "tweet_media_ids": image_ids,
        }
    )

    assert response.status_code == 400

    response_data: dict = response.json()
    assert response_data.get("result") is False


async def test_add_tweet_without_images(
    tweet_data: TweetTestDataClass,
    async_session: AsyncSession,
    async_client: AsyncClient
) -> None:
    response = await async_client.post(
        "tweets/",
        params={"api_key": tweet_data.user.api_key},
        json={
            "tweet_data": tweet_data.content,
            "tweet_media_ids": [],
        }
    )

    assert response.status_code == 201

    response_data: dict = response.json()
    tweet_id: int = response_data.get("tweet_id")

    assert response_data.get("result") is True

    # getting tweet
    tweet_query: Select = (
        select(TweetModel)
        .where(TweetModel.id == tweet_id)
        .where(TweetModel.content == tweet_data.content)
        .where(TweetModel.user_id == tweet_data.user.id)
    )

    tweet: TweetModel = await async_session.scalar(tweet_query)

    # checking existence of the tweet
    assert tweet is not None

    # getting media
    media_query: Select = (
        select(MediaModel)
        .where(MediaModel.tweet_id == tweet_id)
    )

    media_response = await async_session.scalars(media_query)
    media: Sequence[MediaModel] = media_response.fetchall()

    # checking existence of media and count them
    assert len(media) == 0


async def test_add_tweet_with_correct_data(
    tweet_data: TweetTestDataClass,
    image_ids: list[int],
    async_session: AsyncSession,
    async_client: AsyncClient
) -> None:
    response = await async_client.post(
        "tweets/",
        params={"api_key": tweet_data.user.api_key},
        json={
            "tweet_data": tweet_data.content,
            "tweet_media_ids": image_ids,
        }
    )

    assert response.status_code == 201

    response_data: dict = response.json()
    tweet_id: int = response_data.get("tweet_id")

    assert response_data.get("result") is True

    # getting tweet
    tweet_query: Select = (
        select(TweetModel)
        .where(TweetModel.id == tweet_id)
        .where(TweetModel.content == tweet_data.content)
        .where(TweetModel.user_id == tweet_data.user.id)
    )

    tweet: TweetModel = await async_session.scalar(tweet_query)

    # checking existence of the tweet
    assert tweet is not None

    # getting media
    media_query: Select = (
        select(MediaModel)
        .where(MediaModel.tweet_id == tweet_id)
    )

    media_response = await async_session.scalars(media_query)
    media: Sequence[MediaModel] = media_response.fetchall()

    # checking existence of media and count them
    assert len(media) == len(image_ids)
