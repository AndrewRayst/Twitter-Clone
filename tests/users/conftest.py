import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import UserFollowerModel
from tests.shared import TUsersTest


@pytest.fixture(scope="module")
async def followed_users(users: TUsersTest, async_session: AsyncSession) -> TUsersTest:
    """
    The fixture for follow one user by another user.
    :param async_session: session for connecting to database.
    :param users: generated API keys for two users.
    :return: generated API keys for two users.
    """
    instance: UserFollowerModel = UserFollowerModel(
        user_id=users[0].id,
        follower_id=users[1].id,
    )
    async_session.add(instance)
    await async_session.commit()

    return users
