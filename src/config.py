import os

from dotenv import load_dotenv

load_dotenv("./environments/.env")

TESTING: bool = os.getenv("TESTING", False) == "True"

DEBUG: bool = os.getenv("FASTAPI_DEBUG", False) == "True"
STATIC_FILES_PATH: str = os.getenv("FASTAPI_STATIC_FILES_PATH", "static")

SENTRY_DNS: str = os.getenv("SENTRY_DNS", "")

YANDEX_S3_ACCESS_KEY_ID: str = os.getenv("YANDEX_S3_ACCESS_KEY_ID", "")
YANDEX_S3_SECRET_ACCESS_KEY: str = os.getenv("YANDEX_S3_SECRET_ACCESS_KEY", "")
YANDEX_S3_ENDPOINT: str = os.getenv("YANDEX_S3_ENDPOINT", "")
YANDEX_S3_REGION_NAME: str = os.getenv("YANDEX_S3_REGION_NAME", "")

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

ALEMBIC_DB_URL_DEV = "postgresql+asyncpg://{}:{}@0.0.0.0:5432/{}?async_fallback=True".format(
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_DB,
)

ALEMBIC_DB_URL_PROD = "postgresql+asyncpg://{}:{}@database:5432/{}?async_fallback=True".format(
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_DB,
)


REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT: str = os.getenv("REDIS_MASTER_PORT_NUMBER", "6379")
REDIS_USER: str = os.getenv("REDIS_USER", "")
REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "")

REDIS_URL: str = f"redis://{REDIS_USER}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}"
REDIS_URL_TEST: str = f"redis://{REDIS_USER}:{REDIS_PASSWORD}@0.0.0.0:{REDIS_PORT}"
