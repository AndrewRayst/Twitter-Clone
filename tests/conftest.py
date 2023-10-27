from asyncio import get_event_loop_policy, AbstractEventLoop, AbstractEventLoopPolicy
from random import randint
from typing import AsyncGenerator, Generator

import pytest

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool
from httpx import AsyncClient

from src.media.models import MediaModel
from src.utils import get_random_string
from tests.shared import TUsersTest, UserTestDataClass
from src import config
from src.database.core import get_session
from src.database.models import BaseModel
from src.main import application
from src.users.models import UserModel

engine_test: AsyncEngine = create_async_engine(url=config.DB_URL_TEST, poolclass=NullPool)
session_maker = async_sessionmaker(bind=engine_test, expire_on_commit=False)
BaseModel.bind = engine_test


async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        yield session

application.dependency_overrides[get_session] = override_get_session


@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=application, base_url="http://localhost:5000/api") as async_client:
        yield async_client


@pytest.fixture(scope="module")
async def async_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        yield session


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
        users[2].id = user_3.id

        await session.commit()

    return users


@pytest.fixture(scope="module")
async def image_ids(async_session: AsyncSession, users: TUsersTest) -> list[int]:
    """
    The fixture for getting ids of images.
    :return: images ids
    """
    images: list[MediaModel] = [
        MediaModel(src=get_random_string(), user_id=users[0].id)
        for _ in range(randint(0, 3))
    ]

    async_session.add_all(images)
    await async_session.commit()

    return [i_image.id for i_image in images]


# SETUP
@pytest.fixture(scope="session")
def event_loop() -> Generator[AbstractEventLoop, None, None]:
    policy: AbstractEventLoopPolicy = get_event_loop_policy()
    loop: AbstractEventLoop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True, scope="session")
async def prepare_db() -> AsyncGenerator[None, None]:
    async with engine_test.begin() as connect:
        await connect.run_sync(BaseModel.metadata.create_all)
    yield
    async with engine_test.begin() as connect:
        await connect.run_sync(BaseModel.metadata.drop_all)
