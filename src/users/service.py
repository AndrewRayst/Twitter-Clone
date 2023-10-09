from sqlalchemy import Delete, Select, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import ConflictError, ExistError
from src.users.models import UserFollowerModel, UserModel
from src.utils import get_hash


async def follow_user(
    session: AsyncSession, user_id: int, follower_api_key: str
) -> None:
    """
    The service for following user
    :param session: session to connect to the database
    :param user_id: id of the user to follow
    :param follower_api_key: API key of the user who wants to follow
    :return: None
    """
    # Getting follower
    follower_query: Select = select(UserModel).where(
        UserModel.api_key_hash == get_hash(follower_api_key)
    )
    follower: UserModel = await session.scalar(follower_query)

    # Checking the existence of a follower
    if not follower:
        raise ExistError("The follower doesn't exist")

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
    session: AsyncSession, user_id: int, follower_api_key: str
) -> None:
    """
    The service for unfollowing user
    :param session: session to connect to the database
    :param user_id: id of the user to unfollow
    :param follower_api_key: API key of the user who wants to unfollow
    :return: None
    """
    # Getting follower
    follower_query: Select = select(UserModel).where(
        UserModel.api_key_hash == get_hash(follower_api_key)
    )

    follower: UserModel = await session.scalar(follower_query)

    # Checking the existence of a follower
    if not follower:
        raise ExistError("The follower doesn't exist")

    # deleting follow
    statement: Delete = (
        delete(UserFollowerModel)
        .where(UserFollowerModel.user_id == user_id)
        .where(UserFollowerModel.follower_id == follower.id)
    )

    await session.execute(statement)
    await session.commit()
