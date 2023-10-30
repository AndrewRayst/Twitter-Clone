from sqlalchemy import Delete, Select, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.exceptions import ConflictError, ExistError
from src.users.models import UserFollowerModel, UserModel
from src.utils import get_hash


async def get_me(session: AsyncSession, api_key: str) -> UserModel:
    """
    The service for getting your profile
    :param session: session to connect to the database
    :param api_key: API key of the user who wants to get their profile
    :return: user with followers and following
    """
    # Getting user
    query: Select = (
        select(UserModel)
        .where(UserModel.api_key_hash == get_hash(api_key))
        .options(joinedload(UserModel.followers))
        .options(joinedload(UserModel.following))
    )
    user: UserModel = await session.scalar(query)

    # Checking the existence of a user
    if not user:
        raise ExistError("The user doesn't exist")

    return user


async def get_user(session: AsyncSession, user_id: int) -> UserModel:
    """
    The service for getting user profile by id
    :param session: session to connect to the database
    :param user_id: id of the user whose profile you want to get
    :return: user with followers and following
    """
    # Getting user
    query: Select = (
        select(UserModel)
        .where(UserModel.id == user_id)
        .options(joinedload(UserModel.followers))
        .options(joinedload(UserModel.following))
    )
    user: UserModel = await session.scalar(query)

    # Checking the existence of a user
    if not user:
        raise ExistError("The user doesn't exist")

    return user


async def get_user_by_api_key(api_key: str, session: AsyncSession) -> UserModel:
    """
    the service for getting user from the database by api key.
    :param api_key: API key of the user.
    :param session: session to connect to the database.
    :return: user model
    """
    # Getting user
    query: Select = select(UserModel).where(UserModel.api_key_hash == get_hash(api_key))
    return await session.scalar(query)


async def check_and_get_user_by_api_key(
    api_key: str,
    session: AsyncSession,
    error_message: str = "The user doesn't exist",
) -> UserModel:
    """
    the service for checking an existence of the user and
    getting user from the database by api key.
    if the user is not found, an error is thrown.
    :param api_key: API key of the user.
    :param session: session to connect to the database.
    :param error_message: message that will be added to the exception
    if the user is not found
    :return: user model
    """
    # Getting user
    user: UserModel = await get_user_by_api_key(api_key=api_key, session=session)
    # Checking the existence of the user
    if not user:
        raise ExistError(error_message)
    return user


async def follow_user(session: AsyncSession, user_id: int, follower: UserModel) -> None:
    """
    The service for following user
    :param session: session to connect to the database
    :param user_id: id of the user to follow
    :param follower: the user who wants to follow
    :return: None
    """
    # Checking that the user and the follower are different people
    if user_id == follower.id:
        raise ConflictError("The user can't follow himself.")

    # Getting user
    user_query: Select = select(UserModel).where(UserModel.id == user_id)
    user: UserModel = await session.scalar(user_query)

    # Checking the existence of a user
    if not user:
        raise ExistError("The user doesn't exist")

    # Adding follow
    instance: UserFollowerModel = UserFollowerModel(
        user_id=user_id, follower_id=follower.id
    )

    session.add(instance)
    await session.commit()


async def unfollow_user(
    session: AsyncSession, user_id: int, follower: UserModel
) -> None:
    """
    The service for unfollowing user
    :param session: session to connect to the database
    :param user_id: id of the user to unfollow
    :param follower: the user who wants to unfollow
    :return: None
    """
    # deleting follow
    statement: Delete = (
        delete(UserFollowerModel)
        .where(UserFollowerModel.user_id == user_id)
        .where(UserFollowerModel.follower_id == follower.id)
    )

    await session.execute(statement)
    await session.commit()
