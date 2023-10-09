import pytest

from src.users.models import UserModel
from tests.conftest import session_maker
from src.utils import get_hash, get_random_string


@pytest.fixture(scope="session")
async def users() -> tuple[str, str]:
    """
    The fixture for adding two users to db for testing.
    :return: generated API keys for two users.
    """
    api_keys: tuple[str, str] = (
        get_random_string(),
        get_random_string()
    )

    users: list[dict] = [
        {
            "name": get_random_string(),
            "api_key_hash": get_hash(api_keys[i_index])
        }
        for i_index in range(2)
    ]

    async with session_maker() as session:
        user_1 = UserModel(**users[0])
        user_2 = UserModel(**users[1])

        session.add(user_1)
        session.add(user_2)

        await session.commit()

    return api_keys