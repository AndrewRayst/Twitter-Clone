import pytest

from src.users.models import UserFollowerModel
from tests.conftest import session_maker
from tests.shared import TUsersTest


@pytest.fixture(scope="module")
async def followed_users(users: TUsersTest) -> TUsersTest:
    """
    The fixture for follow one user by another user.
    :param users: generated API keys for two users.
    :return: generated API keys for two users.
    """
    async with session_maker() as session:
        instance: UserFollowerModel = UserFollowerModel(
            user_id=users[0].id,
            follower_id=users[1].id,
        )
        session.add(instance)
        await session.commit()

    return users
