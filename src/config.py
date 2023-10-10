import os

from dotenv import load_dotenv

load_dotenv()

DEBUG: bool = bool(os.getenv("FASTAPI_DEBUG", False))
STATIC_FILES_PATH: str = os.getenv("FASTAPI_STATIC_FILES_PATH", "../static")

POSTGRES_USER: str = os.getenv("POSTGRES_USER", "")
POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "")
POSTGRES_DB: str = os.getenv("POSTGRES_DB", "")
POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "0.0.0.0")
DB_URL: str = "postgresql+asyncpg://{}:{}@database:5432/{}".format(
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_DB,
)
DB_URL_TEST: str = "postgresql+asyncpg://{}:{}@{}:5432/{}".format(
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
    POSTGRES_DB,
)
