from httpx import AsyncClient

from tests.shared import TUsersTest, TweetTestDataClass


# test like

async def test_like_with_wrong_user(
        async_client: AsyncClient, tweet: TweetTestDataClass
) -> None:
    """
    Test for checking endpoint with wrong user api key.
    :param async_client: async_client: client for requesting.
    :param tweet: generated tweet
    :return: None
    """
    response = await async_client.post(
        f"tweets/{tweet.id}/likes",
        params={
            "api_key": ""
        }
    )

    assert response.status_code == 400
    assert response.json().get("result") is False


async def test_like_without_user(
        async_client: AsyncClient, tweet: TweetTestDataClass
) -> None:
    """
    Test for checking endpoint without user.
    :param async_client: async_client: client for requesting.
    :param tweet: generated tweet
    :return: None
    """
    response = await async_client.post(f"tweets/{tweet.id}/likes")
    assert response.status_code == 422


async def test_like_with_wrong_tweet_id(
        async_client: AsyncClient, users: TUsersTest
) -> None:
    """
    Test for checking endpoint with wrong tweet id.
    :param async_client: async_client: client for requesting.
    :param users: generated users
    :return: None
    """
    response = await async_client.post(
        "tweets/0/likes",
        params={
            "api_key": users[0].api_key
        }
    )

    assert response.status_code == 400
    assert response.json().get("result") is False


async def test_like_with_correct_data(
        async_client: AsyncClient, tweet: TweetTestDataClass, users: TUsersTest
) -> None:
    """
    Test for checking endpoint with correct data.
    :param async_client: async_client: client for requesting.
    :param tweet: generated tweet
    :param users: generated users
    :return: None
    """
    response = await async_client.post(
        f"tweets/{tweet.id}/likes",
        params={
            "api_key": users[0].api_key
        }
    )

    assert response.status_code == 201
    assert response.json().get("result") is True


async def test_like_twice(
        async_client: AsyncClient, tweet: TweetTestDataClass, users: TUsersTest
) -> None:
    """
    Test for checking endpoint with correct data twice.
    :param async_client: async_client: client for requesting.
    :param tweet: generated tweet
    :param users: generated users
    :return: None
    """
    response = await async_client.post(
        f"tweets/{tweet.id}/likes",
        params={
            "api_key": users[0].api_key
        }
    )

    assert response.status_code == 409
    assert response.json().get("result") is False


# test unlike

async def test_unlike_with_wrong_user(
        async_client: AsyncClient, tweet: TweetTestDataClass
) -> None:
    """
    Test for checking endpoint with wrong user api key.
    :param async_client: async_client: client for requesting.
    :param tweet: generated tweet
    :return: None
    """
    response = await async_client.delete(
        f"tweets/{tweet.id}/likes",
        params={
            "api_key": ""
        }
    )

    assert response.status_code == 400
    assert response.json().get("result") is False


async def test_unlike_without_user(
        async_client: AsyncClient, tweet: TweetTestDataClass
) -> None:
    """
    Test for checking endpoint without user api key.
    :param async_client: async_client: client for requesting.
    :param tweet: generated tweet
    :return: None
    """
    response = await async_client.delete(f"tweets/{tweet.id}/likes")
    assert response.status_code == 422


async def test_unlike_with_wrong_tweet_id(
        async_client: AsyncClient, tweet: TweetTestDataClass, users: TUsersTest
) -> None:
    """
    Test for checking endpoint with wrong tweet id.
    :param async_client: async_client: client for requesting.
    :param tweet: generated tweet
    :param users: generated users
    :return: None
    """
    response = await async_client.delete(
        "tweets/0/likes",
        params={
            "api_key": users[0].api_key
        }
    )

    assert response.status_code == 400
    assert response.json().get("result") is False


async def test_unlike_with_correct_data(
        async_client: AsyncClient, tweet: TweetTestDataClass, users: TUsersTest
) -> None:
    """
    Test for checking endpoint with correct data.
    :param async_client: async_client: client for requesting.
    :param tweet: generated tweet
    :param users: generated users
    :return: None
    """
    response = await async_client.delete(
        f"tweets/{tweet.id}/likes",
        params={
            "api_key": users[0].api_key
        }
    )

    assert response.status_code == 200
    assert response.json().get("result") is True
