import os

from dotenv import load_dotenv

load_dotenv()

DEBUG: bool = bool(os.getenv("FASTAPI_DEBUG", False))
