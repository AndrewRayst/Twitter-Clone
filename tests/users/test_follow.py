from httpx import AsyncClient


async def test_follow_yourself(async_client: AsyncClient, users: tuple[str, str]) -> None:
    """
    Test to check the inability to follow yourself
    :param async_client: client for requesting.
    :param users: generated API keys for two users.
    :return: None
    """
    response = await async_client.post("users/1/follow", params={
        "api_key": users[0]
    })

    assert response.status_code == 400


async def test_follow_non_existent_user(async_client: AsyncClient, users: tuple[str, str]) -> None:
    """
    Test to check the inability to follow a non-existent user
    :param async_client: client for requesting.
    :param users: generated API keys for two users.
    :return: None
    """
    response = await async_client.post("users/404/follow", params={
        "api_key": users[0]
    })

    assert response.status_code == 400


async def test_follow_with_wrong_api_key(async_client: AsyncClient, users: tuple[str, str]) -> None:
    """
    Test to check the inability to follow without the correct api key
    :param async_client: client for requesting.
    :param users: generated API keys for two users.
    :return: None
    """
    response = await async_client.post("users/2/follow", params={
        "api_key": ""
    })

    assert response.status_code == 400


async def test_follow_without_api_key(async_client: AsyncClient, users: tuple[str, str]) -> None:
    """
    Test to check the inability to follow without the api key
    :param async_client: client for requesting.
    :param users: generated API keys for two users.
    :return: None
    """
    response = await async_client.post("users/2/follow")
    assert response.status_code == 422


async def test_follow_with_correct_data(async_client: AsyncClient, users: tuple[str, str]) -> None:
    """
    Test to follow a user
    :param async_client: client for requesting.
    :param users: generated API keys for two users.
    :return: None
    """
    response = await async_client.post("users/2/follow", params={
        "api_key": users[0]
    })

    assert response.status_code == 201


async def test_follow_twice(async_client: AsyncClient, users: tuple[str, str]) -> None:
    """
    Test to check the inability to follow twice
    :param async_client: client for requesting.
    :param users: generated API keys for two users.
    :return: None
    """
    response = await async_client.post("users/2/follow", params={
        "api_key": users[0]
    })

    assert response.status_code == 409
