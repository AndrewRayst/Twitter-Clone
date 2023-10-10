from httpx import AsyncClient

from tests.users.conftest import TUsersTest


async def test_follow_yourself(async_client: AsyncClient, users: TUsersTest) -> None:
    """
    Test to check the inability to follow yourself
    :param async_client: client for requesting.
    :param users: generated API keys for two users.
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
    :param users: generated API keys for two users.
    :return: None
    """
    response = await async_client.post(
        url="users/404/follow",
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
    :param users: generated API keys for two users.
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
    :param users: generated API keys for two users.
    :return: None
    """
    response = await async_client.post(f"users/{users[1].id}/follow")
    assert response.status_code == 422


async def test_follow_with_correct_data(async_client: AsyncClient, users: TUsersTest) -> None:
    """
    Test to follow a user
    :param async_client: client for requesting.
    :param users: generated API keys for two users.
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


async def test_follow_twice(async_client: AsyncClient, users: TUsersTest) -> None:
    """
    Test to check the inability to follow twice
    :param async_client: client for requesting.
    :param users: generated API keys for two users.
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
