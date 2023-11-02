from httpx import AsyncClient

from tests.users.conftest import TUsersTest


async def test_get_my_profile_without_api_key(async_client: AsyncClient) -> None:
    """
    Test for getting own user profile without an api key.
    :param async_client: client for requesting.
    :return: None
    """
    response = await async_client.get("users/me")

    assert response.status_code == 422


async def test_get_my_profile_without_existing_api_key(
    async_client: AsyncClient
) -> None:
    """
    Test for getting own user profile without an existing api key.
    :param async_client: client for requesting.
    :return: None
    """
    response = await async_client.get(
        "users/me",
        headers={
            "Api-Key": ""
        },
    )

    assert response.status_code == 400

    response_json: dict = response.json()
    assert response_json.get("result") is False


async def test_get_my_profile_with_correct_data(
    async_client: AsyncClient, followed_users: TUsersTest
) -> None:
    """
    Test for getting own user profile with correct data.
    :param async_client: client for requesting.
    :param followed_users: generated API keys for two users.
    :return: None
    """
    response = await async_client.get(
        "users/me",
        headers={
            "Api-Key": followed_users[0].api_key
        },
    )

    assert response.status_code == 200

    response_json: dict = response.json()
    assert response_json.get("result") is True

    user: dict = response_json.get("user")
    followers: list[dict] = user.get("followers")
    following: list[dict] = user.get("following")

    assert len(followers) == 1
    assert len(following) == 0

    assert followers[0].get("id") == followed_users[1].id
    assert followers[0].get("name") == followed_users[1].name
