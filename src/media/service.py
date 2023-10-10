from sqlalchemy import Select, select
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
    instance: MediaModel = MediaModel(src=image_src)
    session.add(instance)
    await session.commit()

    return instance.id
