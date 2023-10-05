import os

from dotenv import load_dotenv

load_dotenv()

DEBUG: bool = bool(os.getenv("FASTAPI_DEBUG", False))

POSTGRES_USER = os.getenv("POSTGRES_USER", "")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
POSTGRES_DB = os.getenv("POSTGRES_DB", "")
DB_URL: str = "postgresql+asyncpg://{}:{}@database:5432/{}".format(
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_DB,
)
