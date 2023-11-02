from typing import Sequence

from sqlalchemy import (
    Delete,
    ScalarResult,
    Select,
    Subquery,
    delete,
    desc,
    func,
    or_,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.exceptions import AccessError, ExistError
from src.media.models import MediaModel
from src.tweets.models import TweetLikeModel, TweetModel
from src.users.models import UserModel
from src.utils import get_hash


async def get_tweet(session: AsyncSession, tweet_id: int) -> TweetModel:
    """
    The service for getting the tweet by id
    :param session: session to connect to the database
    :param tweet_id: id of tweet.
    :return: tweet model
    """
    # Getting the tweet
    tweet_query: Select = select(TweetModel).where(TweetModel.id == tweet_id)
    return await session.scalar(tweet_query)


async def check_and_get_tweet(
    session: AsyncSession, tweet_id: int, error_message: str = "the tweet doesn't exist"
) -> TweetModel:
    tweet: TweetModel = await get_tweet(session=session, tweet_id=tweet_id)
    if not tweet:
        raise ExistError(error_message)
    return tweet


async def get_tweets(
    session: AsyncSession,
    api_key: str,
    limit: int,
    offset: int,
) -> list[TweetModel] | Sequence[TweetModel]:
    """
    The service for adding tweet in database
    :param session: session to connect to the database.
    :param api_key: API key of the user who wants to add the tweet
    :param limit: limiting the number of tweets to receive
    :param offset: number of posts to skip
    :return: id of the tweet in database
    """
    # Getting user
    user_query: Select = (
        select(UserModel)
        .where(UserModel.api_key_hash == get_hash(api_key))
        .options(joinedload(UserModel.following))
    )
    user: UserModel = await session.scalar(user_query)

    # Checking the existence of a user
    if not user:
        raise ExistError("The user who wants to retrieve tweets doesn't exist")

    # getting user following ids
    user_following_ids: list[int] = [i_following.id for i_following in user.following]

    # Subquery for getting tweets
    tweets_subquery: Subquery = (
        select(TweetModel.content, TweetModel.id.label("id"))
        # adding author
        .options(joinedload(TweetModel.author).load_only(UserModel.id, UserModel.name))
        # adding likes
        .options(joinedload(TweetModel.likes).load_only(UserModel.id, UserModel.name))
        # adding media
        .options(joinedload(TweetModel.media).load_only(MediaModel.src))
        # sorting for getting the latest tweets
        .order_by(TweetModel.id.desc())
        # filtering to get only your tweets or tweets from people you follow
        .where(
            or_(
                TweetModel.user_id == user.id,
                TweetModel.user_id.in_(user_following_ids),
            )
        )
        # offset and limit tweets
        .subquery()
    )

    subquery: Subquery
    if limit and offset:
        subquery = (
            select(tweets_subquery)
            .offset(offset=(offset - 1) * limit)
            .limit(limit=limit)
            .subquery()
        )
    else:
        subquery = tweets_subquery

    # Subquery for getting count of likes
    likes_count_subquery: Subquery = (
        select(
            TweetModel.id.label("tweet_id"),
            func.count(TweetLikeModel.id).label("likes_count"),
        )
        .outerjoin(TweetLikeModel)
        .join(subquery, TweetModel.id == subquery.c.id)
        .group_by(TweetModel.id)
        .subquery("likes_count_subquery")
    )

    # Query for getting tweets and order by likes
    query: Select = (
        select(TweetModel)
        # adding tweets
        .join(subquery, subquery.c.id == TweetModel.id)
        # adding the number of likes for sorting
        .join(likes_count_subquery, TweetModel.id == likes_count_subquery.c.tweet_id)
        # sorting by number of likes. from most to least.
        .order_by(desc(likes_count_subquery.c.likes_count))
    )

    # getting tweets
    tweets_response: ScalarResult = await session.scalars(query)
    tweets: Sequence = tweets_response.unique().fetchall()

    # # create attachments for every post
    for i_tweet in tweets:
        i_tweet.attachments = [i_media.src for i_media in i_tweet.media]

    return tweets


async def add_tweet(session: AsyncSession, user: UserModel, tweet_content: str) -> int:
    """
    The service for adding tweet in database
    :param session: session to connect to the database.
    :param user: the user who wants to add the tweet
    :param tweet_content: text of the tweet
    :return: id of the tweet in database
    """
    # Adding tweet in database
    instance: TweetModel = TweetModel(user_id=user.id, content=tweet_content)

    session.add(instance)
    await session.commit()

    return instance.id


async def delete_tweet(session: AsyncSession, tweet_id: int, user: UserModel) -> None:
    """
    The service for adding tweet in database
    :param session: session to connect to the database.
    :param user: the user who wants to delete the tweet
    :param tweet_id: ID of the tweet
    :return: id of the tweet in database
    """
    # Getting the tweet by id
    tweet_query: Select = select(TweetModel).where(TweetModel.id == tweet_id)
    tweet: TweetModel = await session.scalar(tweet_query)

    # Checking the existence of a tweet
    if not tweet:
        raise ExistError("The tweet doesn't exist")

    # Checking whether the user has the right to delete a tweet
    if tweet.user_id != user.id:
        raise AccessError("User can't delete this tweet.")

    # Deleting tweet in database
    await session.delete(tweet)
    await session.commit()


async def like_tweet(session: AsyncSession, tweet: TweetModel, user: UserModel) -> None:
    """
    The service for liking the tweet by id
    :param session: session to connect to the database
    :param tweet: tweet to like
    :param user: the user who wants to like the tweet
    :return: None
    """
    # Adding like record
    instance: TweetLikeModel = TweetLikeModel(user_id=user.id, tweet_id=tweet.id)
    session.add(instance)
    await session.commit()


async def unlike_tweet(
    session: AsyncSession, tweet: TweetModel, user: UserModel
) -> None:
    """
    The service for unliking the tweet by id
    :param session: session to connect to the database
    :param tweet: tweet to unlike
    :param user: the user who wants to unlike the tweet
    :return: None
    """
    # Deleting like record
    statement: Delete = (
        delete(TweetLikeModel)
        .where(TweetLikeModel.user_id == user.id)
        .where(TweetLikeModel.tweet_id == tweet.id)
    )

    await session.execute(statement)
    await session.commit()
