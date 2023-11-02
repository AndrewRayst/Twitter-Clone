from httpx import AsyncClient
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import UserFollowerModel
from tests.users.conftest import TUsersTest


async def test_unfollow_with_wrong_api_key(
    async_client: AsyncClient, followed_users: TUsersTest
) -> None:
    """
    Test to check the inability to unfollow without the correct api key
    :param async_client: client for requesting.
    :param followed_users: generated API keys for three users.
    :return: None
    """
    response = await async_client.post(
        url=f"users/{followed_users[1].id}/unfollow",
        headers={
            "Api-Key": ""
        }
    )

    assert response.status_code == 400

    response_json: dict = response.json()
    assert response_json.get("result") is False


async def test_unfollow_without_api_key(
    async_client: AsyncClient, followed_users: TUsersTest
) -> None:
    """
    Test to check the inability to unfollow without the api key
    :param async_client: client for requesting.
    :param followed_users: generated API keys for two users.
    :return: None
    """
    response = await async_client.post(
        url=f"users/{followed_users[1].id}/unfollow"
    )
    assert response.status_code == 422


async def test_unfollow_with_correct_data(
    async_client: AsyncClient, async_session: AsyncSession, followed_users: TUsersTest
) -> None:
    """
    Test to unfollow a user
    :param async_client: client for requesting.
    :param async_session: session for async connecting to the database.
    :param followed_users: generated API keys for two users.
    :return: None
    """
    response = await async_client.post(
        url=f"users/{followed_users[1].id}/unfollow",
        headers={
            "Api-Key": followed_users[0].api_key
        }
    )

    assert response.status_code == 200

    response_json: dict = response.json()
    assert response_json.get("result") is True

    query: Select = (
        select(UserFollowerModel)
        .where(UserFollowerModel.follower_id == followed_users[0].id)
        .where(UserFollowerModel.user_id == followed_users[1].id)
    )
    following_record: UserFollowerModel = await async_session.scalar(query)
    assert following_record is None
