from httpx import AsyncClient
from sqlalchemy import select, Select
from sqlalchemy.ext.asyncio import AsyncSession

from shared import TUsersTest
from src.media.models import MediaModel


async def test_adding_media_with_correct_data(
    async_client: AsyncClient,
    async_session: AsyncSession,
    users: TUsersTest,
    image_data: bytes
) -> None:
    """
    Test to check the inability to follow yourself
    :param async_client: client for requesting.
    :param async_session: session for connecting to database.
    :param users: generated API keys for two users.
    :param image_data: image bytes
    :return: None
    """
    response = await async_client.post(
        f"medias/",
        params={
            "api_key": users[0].api_key
        },
        files={
            "file": image_data
        }
    )

    assert response.status_code == 201

    response_data: dict = response.json()

    query: Select = (
        select(MediaModel)
        .where(MediaModel.id == response_data.get("media_id"))
    )

    media_record: MediaModel = await async_session.scalar(query)

    assert media_record is not None
    assert type(media_record.src) is str
    assert len(media_record.src) > 0
