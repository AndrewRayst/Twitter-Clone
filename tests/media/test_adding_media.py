from httpx import AsyncClient
from sqlalchemy import select, Select
from sqlalchemy.ext.asyncio import AsyncSession

from shared import TUsersTest
from src.media.models import MediaModel


async def test_adding_image_without_user_api_key(
    async_client: AsyncClient,
    image_data: bytes
) -> None:
    """
    Test to checking the endpoint for adding the image without user api key.
    :param async_client: client for requesting.
    :param image_data: image bytes
    :return: None
    """
    response = await async_client.post(
        f"medias/",
        files={
            "file": image_data,
        }
    )

    assert response.status_code == 422


async def test_adding_image_without_existing_user_api_key(
    async_client: AsyncClient,
    image_data: bytes
) -> None:
    """
    Test to checking the endpoint for adding the image without existing user api key.
    :param async_client: client for requesting.
    :param image_data: image bytes
    :return: None
    """
    response = await async_client.post(
        f"medias/",
        headers={
            "Api-Key": "",
        },
        files={
            "file": image_data,
        }
    )

    assert response.status_code == 400
    assert response.json().get("result") is False


async def test_adding_image_with_correct_data(
    async_client: AsyncClient,
    async_session: AsyncSession,
    users: TUsersTest,
    image_data: bytes
) -> None:
    """
    Test to checking the endpoint for adding the image.
    :param async_client: client for requesting.
    :param async_session: session for connecting to database.
    :param users: generated API keys for two users.
    :param image_data: image bytes
    :return: None
    """
    response = await async_client.post(
        f"medias/",
        headers={
            "Api-Key": users[0].api_key
        },
        files={
            "file": image_data
        }
    )

    assert response.status_code == 201

    response_data: dict = response.json()
    assert response_data.get("result") is True

    # getting media record
    query: Select = (
        select(MediaModel)
        .where(MediaModel.id == response_data.get("media_id"))
    )

    media_record: MediaModel = await async_session.scalar(query)

    assert media_record is not None
    assert type(media_record.src) is str
    assert len(media_record.src) > 0
