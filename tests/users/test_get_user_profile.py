from httpx import AsyncClient

from tests.users.conftest import TUsersTest


async def test_get_user_profile_without_api_key(
    async_client: AsyncClient, followed_users: TUsersTest
) -> None:
    """
    Test for getting user profile by id without an api key.
    :param async_client: client for requesting.
    :return: None
    """
    response = await async_client.get(f"users/{followed_users[1].id}")

    assert response.status_code == 422


async def test_get_user_profile_without_existing_api_key(
    async_client: AsyncClient, followed_users: TUsersTest
) -> None:
    """
    Test for getting user profile by id without an existing api key.
    :param async_client: client for requesting.
    :return: None
    """
    response = await async_client.get(
        f"users/{followed_users[1].id}",
        params={
            "api_key": ""
        },
    )

    assert response.status_code == 400

    response_json: dict = response.json()
    assert response_json.get("result") is False


async def test_get_user_profile(
    async_client: AsyncClient, followed_users: TUsersTest
) -> None:
    """
    Test for getting user profile by id with correct data.
    :param async_client: client for requesting.
    :return: None
    """
    response = await async_client.get(
        f"users/{followed_users[1].id}",
        params={
            "api_key": followed_users[0].api_key
        }
    )

    assert response.status_code == 200

    response_json: dict = response.json()
    assert response_json.get("result") is True

    user: dict = response_json.get("user")
    followers: list[dict] = user.get("followers")
    following: list[dict] = user.get("following")

    assert len(followers) == 0
    assert len(following) == 1

    assert following[0].get("id") == followed_users[0].id
    assert following[0].get("name") == followed_users[0].name
