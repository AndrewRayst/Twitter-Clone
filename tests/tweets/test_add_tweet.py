from typing import Sequence

from httpx import AsyncClient
from sqlalchemy import select, Select, func
from sqlalchemy.ext.asyncio import AsyncSession

from shared import TweetTestDataClass, TUsersTest
from src.media.models import MediaModel
from src.tweets.models import TweetModel


async def test_add_tweet_with_another_user(
    tweet_data: TweetTestDataClass,
    image_ids: list[int],
    users: TUsersTest,
    async_session: AsyncSession,
    async_client: AsyncClient
) -> None:
    """
    Test for adding tweet with another user.
    user who didn't add images
    :param tweet_data: data for adding the tweet.
    :param image_ids: the tweet Image IDs.
    :param async_client: client for requesting.
    :param async_session: session for async connecting to the database.
    :return: None
    """
    response = await async_client.post(
        "tweets/",
        params={"api_key": users[1].api_key},
        json={
            "tweet_data": tweet_data.content,
            "tweet_media_ids": image_ids,
        }
    )

    assert response.status_code == 201

    response_data: dict = response.json()
    assert response_data.get("result") is True

    image_count_query: Select = (
        select(func.count(MediaModel.id))
        .where(MediaModel.id.in_(image_ids))
        .where(MediaModel.tweet_id == response_data.get("tweet_id"))
    )
    image_count: int = await async_session.scalar(image_count_query)
    assert image_count == 0


async def test_add_tweet_without_user(
        tweet_data: TweetTestDataClass,
        image_ids: list[int],
        async_session: AsyncSession,
        async_client: AsyncClient
) -> None:
    """
    Test for adding tweet without the user.
    :param tweet_data: data for adding the tweet.
    :param image_ids: the tweet Image IDs.
    :param async_client: client for requesting.
    :param async_session: session for async connecting to the database.
    :return: None
    """
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
    """
    Test for adding tweet without the existing user.
    :param tweet_data: data for adding the tweet.
    :param image_ids: the tweet Image IDs.
    :param async_client: client for requesting.
    :param async_session: session for async connecting to the database.
    :return: None
    """
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
    """
    Test for adding tweet with correct data and without media.
    :param tweet_data: data for adding the tweet.
    :param async_client: client for requesting.
    :param async_session: session for async connecting to the database.
    :return: None
    """
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
    """
    Test for adding tweet with correct data and media.
    :param tweet_data: data for adding the tweet.
    :param image_ids: the tweet Image IDs.
    :param async_client: client for requesting.
    :param async_session: session for async connecting to the database.
    :return: None
    """
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
