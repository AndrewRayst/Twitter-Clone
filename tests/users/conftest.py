import pytest

from src.users.models import UserModel, UserFollowerModel
from tests.conftest import session_maker
from src.utils import get_hash, get_random_string


class UserTestDataClass:
    api_key: str
    api_key_hash: str
    name: str
    id: int = 0

    def __init__(self):
        self.name = get_random_string()
        self.api_key = get_random_string()
        self.api_key_hash = get_hash(self.api_key)

    def __dict__(self) -> dict:
        return {
            "api_key_hash": self.api_key_hash,
            "name": self.name,
        }


TUsersTest = tuple[UserTestDataClass, UserTestDataClass, UserTestDataClass]


@pytest.fixture(scope="module")
async def users() -> TUsersTest:
    """
    The fixture for adding three users to db for testing.
    :return: generated API keys for three users.
    """
    users: TUsersTest = (
        UserTestDataClass(),
        UserTestDataClass(),
        UserTestDataClass(),
    )

    async with session_maker() as session:
        # create users for testing
        user_1 = UserModel(**users[0].__dict__())
        user_2 = UserModel(**users[1].__dict__())
        user_3 = UserModel(**users[2].__dict__())

        # add users to db
        session.add(user_1)
        session.add(user_2)
        session.add(user_3)

        await session.flush()

        # save id
        users[0].id = user_1.id
        users[1].id = user_2.id

        await session.commit()

    return users


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
