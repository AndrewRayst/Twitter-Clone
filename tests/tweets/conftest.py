import pytest
from sqlalchemy import Update, update, Insert, insert
from sqlalchemy.ext.asyncio import AsyncSession

from shared import TweetTestDataClass, TUsersTest
from src.media.models import MediaModel
from src.tweets.models import TweetModel, TweetLikeModel
from src.users.models import UserFollowerModel


@pytest.fixture(scope="function")
async def tweet_data(users: TUsersTest) -> TweetTestDataClass:
    """
    The fixture for getting tweet data
    :param users: user who added in database
    :return: tweet data
    """
    return TweetTestDataClass(users[0])


@pytest.fixture(scope="module")
async def tweet(
    users: TUsersTest,
    image_ids: list[int],
    async_session: AsyncSession
) -> TweetTestDataClass:
    """
    The fixture for adding tweet in database and getting tweet data
    :param users: user who added in database
    :param image_ids: image IDs for tweet
    :param async_session: async session for connecting to database
    :return: tweet data
    """
    tweet = TweetTestDataClass(users[0])
    instance: TweetModel = tweet.get_instance()

    async_session.add(instance)
    await async_session.flush()

    tweet.id = instance.id

    statement: Update = (
        update(MediaModel)
        .where(MediaModel.id.in_(image_ids))
        .values(tweet_id=tweet.id)
    )
    await async_session.execute(statement)

    await async_session.commit()

    return tweet


@pytest.fixture(scope="module")
async def tweets(
    users: TUsersTest,
    async_session: AsyncSession
) -> list[TweetTestDataClass]:
    """
    The fixture for adding tweets in database, following users, liking tweets and getting tweets data
    :param users: user who added in database
    :param async_session: async session for connecting to database
    :return: tweet data
    """
    # create tweets
    # the number of indexes is 25 because it is more than 2 pages with a limit of 10 tweets.
    # The number of tweets from user #1 is 8.
    # The number of tweets from user #2 is 12.
    # The number of tweets from user #3 is 5.
    # User #3's tweets will not be visible to user #1
    # because user #1 does not follow user #3.
    user_indexes: list[int] = [
        0, 0, 0, 1, 1, 1, 0, 0, 1, 0,  1,  1,  1,  0,  0,  1,  1,  2,  1,  2,  2,  2,  2,  1,  1,
    ]

    tweets: list[TweetTestDataClass] = [
        TweetTestDataClass(users[i_index])
        for i_index in user_indexes
    ]

    tweet_instances: list[TweetModel] = [
        i_tweet.get_instance()
        for i_tweet in tweets
    ]

    async_session.add_all(tweet_instances)
    await async_session.flush()

    # updating id for tweets
    for i_index, i_tweet in enumerate(tweets):
        i_tweet.id = tweet_instances[i_index].id

    # following users
    following_statement: Insert = (
        insert(UserFollowerModel)
        .values(user_id=users[1].id, follower_id=users[0].id)
    )

    await async_session.execute(following_statement)

    # liking tweets
    like_instances: list[TweetLikeModel] = [
        TweetLikeModel(tweet_id=tweets[13].id, user_id=users[0].id),
        TweetLikeModel(tweet_id=tweets[13].id, user_id=users[1].id),
        TweetLikeModel(tweet_id=tweets[13].id, user_id=users[2].id),
        TweetLikeModel(tweet_id=tweets[16].id, user_id=users[1].id),
        TweetLikeModel(tweet_id=tweets[16].id, user_id=users[2].id),
        TweetLikeModel(tweet_id=tweets[5].id, user_id=users[1].id),
        TweetLikeModel(tweet_id=tweets[5].id, user_id=users[2].id),
        TweetLikeModel(tweet_id=tweets[3].id, user_id=users[2].id),
    ]

    async_session.add_all(like_instances)
    await async_session.commit()

    return tweets
