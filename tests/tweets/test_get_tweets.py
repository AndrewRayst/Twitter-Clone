from httpx import AsyncClient

from shared import TweetTestDataClass, TUsersTest


async def test_get_5_tweets_with_correct_data(
    tweets: list[TweetTestDataClass],
    users: TUsersTest,
    async_client: AsyncClient,
) -> None:
    """
    Test for checking the endpoint for retrieving 5 tweets.
    :param tweets: tweets which added in database
    :param users: generated users
    :param async_client: client for requesting.
    :return: None
    """
    response = await async_client.get(
        "tweets/",
        headers={"Api-Key": users[0].api_key},
        params={
            "limit": 5,
            "offset": 1,
        },
    )

    assert response.status_code == 200

    response_json: dict = response.json()

    assert response_json.get("result") is True
    assert len(response_json.get("tweets")) == 5


async def test_get_tweets_without_user(async_client: AsyncClient) -> None:
    """
    Test for checking the endpoint for retrieving tweets without user.
    :param async_client: client for requesting.
    :return: None
    """
    response = await async_client.get(
        "tweets/",
        params={
            "limit": 10,
            "offset": 1,
        }
    )

    assert response.status_code == 422


async def test_get_tweets_without_existing_user(async_client: AsyncClient) -> None:
    """
    Test for checking the endpoint for retrieving tweets without existing user.
    :param async_client: client for requesting.
    :return: None
    """
    response = await async_client.get(
        "tweets/",
        headers={"Api-Key": ""},
        params={
            "limit": 10,
            "offset": 1,
        },
    )

    assert response.status_code == 400
    assert response.json().get("result") is False


async def test_get_tweets_without_limit_and_offset(
    tweets: list[TweetTestDataClass],
    users: TUsersTest,
    async_client: AsyncClient,
) -> None:
    """
    Test for checking the endpoint for retrieving tweets without limit and offset.
    :param tweets: tweets which added in database
    :param users: generated users
    :param async_client: client for requesting.
    :return: None
    """
    response = await async_client.get(
        "tweets/",
        headers={
            "Api-Key": users[0].api_key,
        }
    )

    assert response.status_code == 200
    assert response.json().get("result") is True


async def test_get_tweets_with_negative_limit(
    tweets: list[TweetTestDataClass],
    users: TUsersTest,
    async_client: AsyncClient,
) -> None:
    """
    Test for checking the endpoint for retrieving tweets with negative limit.
    :param tweets: tweets which added in database
    :param users: users who added in database
    :param async_client: client for requesting.
    :return: None
    """
    response = await async_client.get(
        "tweets/",
        headers={"Api-Key": users[0].api_key},
        params={
            "limit": -1,
            "offset": 1,
        },
    )

    assert response.status_code == 400
    assert response.json().get("result") is False


async def test_get_tweets_with_limit_greater_20(
    tweets: list[TweetTestDataClass],
    users: TUsersTest,
    async_client: AsyncClient,
) -> None:
    """
    Test for checking the endpoint for retrieving tweets with limit greater than 20.
    :param tweets: tweets which added in database
    :param users: users who added in database
    :param async_client: client for requesting.
    :return: None
    """
    response = await async_client.get(
        "tweets/",
        headers={"Api-Key": users[0].api_key},
        params={
            "limit": 21,
            "offset": 1,
        },
    )

    assert response.status_code == 400
    assert response.json().get("result") is False


async def test_get_tweets_with_offset_less_than_1(
    tweets: list[TweetTestDataClass],
    users: TUsersTest,
    async_client: AsyncClient
) -> None:
    """
    Test for checking the endpoint for retrieving tweets with offset less than 1.
    :param tweets: tweets which added in database
    :param users: users who added in database
    :param async_client: client for requesting.
    :return: None
    """
    response = await async_client.get(
        "tweets/",
        headers={"Api-Key": users[0].api_key},
        params={
            "limit": 10,
            "offset": 0,
        },
    )

    assert response.status_code == 400
    assert response.json().get("result") is False


async def test_get_tweets_with_correct_data_page_1(
    tweets: list[TweetTestDataClass],
    users: TUsersTest,
    async_client: AsyncClient,
) -> None:
    """
    Test for checking the endpoint for retrieving tweets with pagination. Page #1.
    :param tweets: tweets which added in database
    :param users: users who added in database
    :param async_client: client for requesting.
    :return: None
    """
    response = await async_client.get(
        "tweets/",
        headers={"Api-Key": users[0].api_key},
        params={
            "limit": 10,
            "offset": 1,
        },
    )

    assert response.status_code == 200

    response_json: dict = response.json()
    response_tweets: list[dict] = response_json.get("tweets")

    # checking result and tweets count
    assert response_json.get("result") is True
    assert len(response_tweets) == 10

    # checking tweets order by likes number
    assert response_tweets[0].get("id") == tweets[13].id
    assert response_tweets[1].get("id") == tweets[16].id

    # checking tweet ids
    response_tweets_ids = [i_tweet.get("id") for i_tweet in response_tweets]
    for i_index in [24, 23, 18, 16, 15, 14, 13, 12, 11, 10]:
        assert tweets[i_index].id in response_tweets_ids

    # checking authors
    author_ids: list[int] = [
        i_tweet.get("author").get("id") for i_tweet in response_tweets
    ]

    assert users[0].id in author_ids
    assert users[1].id in author_ids
    assert users[2].id not in author_ids


async def test_get_tweets_with_correct_data_page_2(
    tweets: list[TweetTestDataClass],
    users: TUsersTest,
    async_client: AsyncClient,
) -> None:
    """
    Test for checking the endpoint for retrieving tweets with pagination. Page #2.
    :param tweets: tweets which added in database
    :param users: users who added in database
    :param async_client: client for requesting.
    :return: None
    """
    response = await async_client.get(
        "tweets/",
        headers={"Api-Key": users[0].api_key},
        params={
            "limit": 10,
            "offset": 2,
        },
    )

    assert response.status_code == 200

    response_json: dict = response.json()
    response_tweets: list[dict] = response_json.get("tweets")

    # checking result and tweets count
    assert response_json.get("result") is True
    assert len(response_tweets) == 10

    # checking tweets order by likes number
    assert response_tweets[0].get("id") == tweets[5].id
    assert response_tweets[1].get("id") == tweets[3].id

    # checking tweet ids
    response_tweets_ids = [i_tweet.get("id") for i_tweet in response_tweets]
    for i_index in [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]:
        assert tweets[i_index].id in response_tweets_ids

    # checking authors
    author_ids: list[int] = [
        i_tweet.get("author").get("id") for i_tweet in response_tweets
    ]

    assert users[0].id in author_ids
    assert users[1].id in author_ids
    assert users[2].id not in author_ids
