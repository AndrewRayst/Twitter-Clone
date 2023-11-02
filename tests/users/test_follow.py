from httpx import AsyncClient
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import UserFollowerModel
from tests.users.conftest import TUsersTest


# test follow

async def test_follow_yourself(async_client: AsyncClient, users: TUsersTest) -> None:
    """
    Test to check the inability to follow yourself
    :param async_client: client for requesting.
    :param users: generated API keys for three users.
    :return: None
    """
    response = await async_client.post(
        url=f"users/{users[0].id}/follow",
        params={
            "api_key": users[0].api_key
        }
    )

    assert response.status_code == 400

    response_json: dict = response.json()
    assert response_json.get("result") is False


async def test_follow_non_existent_user(async_client: AsyncClient, users: TUsersTest) -> None:
    """
    Test to check the inability to follow a non-existent user
    :param async_client: client for requesting.
    :param users: generated API keys for three users.
    :return: None
    """
    response = await async_client.post(
        url="users/404040404/follow",
        params={
            "api_key": users[0].api_key
        }
    )

    assert response.status_code == 400

    response_json: dict = response.json()
    assert response_json.get("result") is False


async def test_follow_with_wrong_api_key(async_client: AsyncClient, users: TUsersTest) -> None:
    """
    Test to check the inability to follow without the correct api key
    :param async_client: client for requesting.
    :param users: generated API keys for three users.
    :return: None
    """
    response = await async_client.post(
        url=f"users/{users[1].id}/follow",
        params={
            "api_key": ""
        }
    )

    assert response.status_code == 400

    response_json: dict = response.json()
    assert response_json.get("result") is False


async def test_follow_without_api_key(async_client: AsyncClient, users: TUsersTest) -> None:
    """
    Test to check the inability to follow without the api key
    :param async_client: client for requesting.
    :param users: generated API keys for three users.
    :return: None
    """
    response = await async_client.post(f"users/{users[1].id}/follow")
    assert response.status_code == 422


async def test_follow_with_correct_data(
    async_client: AsyncClient, async_session: AsyncSession, users: TUsersTest
) -> None:
    """
    Test to follow a user
    :param async_client: client for requesting.
    :param async_session: session for async connecting to the database.
    :param users: generated API keys for three users.
    :return: None
    """
    response = await async_client.post(
        url=f"users/{users[1].id}/follow",
        params={
            "api_key": users[0].api_key
        }
    )

    assert response.status_code == 201

    response_json: dict = response.json()
    assert response_json.get("result") is True

    query: Select = (
        select(UserFollowerModel)
        .where(UserFollowerModel.follower_id == users[0].id)
        .where(UserFollowerModel.user_id == users[1].id)
    )
    following_record: UserFollowerModel = await async_session.scalar(query)
    assert following_record is not None


async def test_follow_twice(
    async_client: AsyncClient, async_session: AsyncSession, users: TUsersTest
) -> None:
    """
    Test to check the inability to follow twice
    :param async_client: client for requesting.
    :param async_session: session for async connecting to the database.
    :param users: generated API keys for three users.
    :return: None
    """
    response = await async_client.post(
        url=f"users/{users[1].id}/follow",
        params={
            "api_key": users[0].api_key
        }
    )

    assert response.status_code == 409

    response_json: dict = response.json()
    assert response_json.get("result") is False

    query: Select = (
        select(UserFollowerModel)
        .where(UserFollowerModel.follower_id == users[0].id)
        .where(UserFollowerModel.user_id == users[1].id)
    )
    following_record: UserFollowerModel = await async_session.scalar(query)
    assert following_record is not None
