import os

from dotenv import load_dotenv

load_dotenv()

TESTING: bool = os.getenv("TESTING", False) == "True"

DEBUG: bool = os.getenv("FASTAPI_DEBUG", False) == "True"
STATIC_FILES_PATH: str = os.getenv("FASTAPI_STATIC_FILES_PATH", "static")

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

REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT: str = os.getenv("REDIS_MASTER_PORT_NUMBER", "6379")
REDIS_URL: str = f"redis://{REDIS_HOST}:{REDIS_PORT}"
REDIS_URL_TEST: str = f"redis://0.0.0.0:{REDIS_PORT}"
