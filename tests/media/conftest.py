import aiofiles
import pytest


@pytest.fixture(scope="session")
async def image_data() -> bytes:
    async with aiofiles.open("tests/media/test_image.jpg", "rb") as file:
        return await file.read()
