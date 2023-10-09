from httpx import AsyncClient


async def test_unfollow_with_wrong_api_key(async_client: AsyncClient, users: tuple[str, str]) -> None:
    """
    Test to check the inability to unfollow without the correct api key
    :param async_client: client for requesting.
    :param users: generated API keys for two users.
    :return: None
    """
    response = await async_client.post("users/2/unfollow", params={
        "api_key": ""
    })

    assert response.status_code == 400


async def test_unfollow_without_api_key(async_client: AsyncClient, users: tuple[str, str]) -> None:
    """
    Test to check the inability to unfollow without the api key
    :param async_client: client for requesting.
    :param users: generated API keys for two users.
    :return: None
    """
    response = await async_client.post("users/2/unfollow")
    assert response.status_code == 422


async def test_unfollow_with_correct_data(async_client: AsyncClient, users: tuple[str, str]) -> None:
    """
    Test to unfollow a user
    :param async_client: client for requesting.
    :param users: generated API keys for two users.
    :return: None
    """
    response = await async_client.post("users/2/unfollow", params={
        "api_key": users[0]
    })

    assert response.status_code == 200
