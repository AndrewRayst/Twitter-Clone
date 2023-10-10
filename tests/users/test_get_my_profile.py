from httpx import AsyncClient

from tests.users.conftest import TUsersTest


async def test_get_my_profile(
    async_client: AsyncClient, followed_users: TUsersTest
) -> None:
    response = await async_client.get(
        "users/me",
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

    assert len(followers) == 1
    assert len(following) == 0

    assert followers[0].get("id") == followed_users[1].id
    assert followers[0].get("name") == followed_users[1].name
