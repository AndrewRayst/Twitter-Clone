from sqlalchemy import Select, Update, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import ExistError
from src.media.models import MediaModel
from src.users.models import UserModel
from src.utils import get_hash


async def add_image_media(session: AsyncSession, api_key: str, image_src: str) -> int:
    """
    The service for adding image media to the database.
    :param session: session to connect to the database.
    :param api_key: API key of the user who wants to add image media.
    :param image_src: source where locate image media is located.
    :return: image media id in database.
    """
    # Getting user who wants to add image media
    query: Select = select(UserModel).where(UserModel.api_key_hash == get_hash(api_key))

    user: UserModel = await session.scalar(query)

    # Checking the existence of a user
    if not user:
        raise ExistError("The user who wants to add image media doesn't exist")

    # Adding image to database
    instance: MediaModel = MediaModel(src=image_src, user_id=user.id)
    session.add(instance)
    await session.commit()

    return instance.id


async def update_tweet_id(
    session: AsyncSession, tweet_id: int, api_key: str, media_ids: list[int]
) -> None:
    """
    The service for updating the twitter_id column
    in records of 'media' table by the transmitted identifiers.
    :param session: session to connect to the database.
    :param tweet_id: tweet ID for attaching media files
    :param api_key: API key of the user who wants to update tweet_id.
    :param media_ids: media IDs for attaching to a tweet
    :return: None
    """
    # Getting user who wants to update tweet_id
    query: Select = select(UserModel).where(UserModel.api_key_hash == get_hash(api_key))

    user: UserModel = await session.scalar(query)

    # Checking the existence of a user
    if not user:
        raise ExistError("The user doesn't exist")

    # updating tweet_id
    statement: Update = (
        update(MediaModel)
        .where(MediaModel.user_id == user.id)
        .where(MediaModel.id.in_(media_ids))
        .where(MediaModel.tweet_id.is_(None))
        .values(tweet_id=tweet_id)
    )
    await session.execute(statement)
    await session.commit()


async def update_image_src(
    session: AsyncSession, image_id: int, image_src: str
) -> None:
    """
    The service for updating the src column
    in records of 'media' table by the transmitted identifiers.
    !!! Don't use this without checking for the existence of
        a user with the passed api_key !!!
    :param session: session to connect to the database.
    :param image_id: image ID for updating source
    :param image_src: new image source
    :return: None
    """
    # update image src
    statement: Update = (
        update(MediaModel).where(MediaModel.id == image_id).values(src=image_src)
    )
    await session.execute(statement)
    await session.commit()
