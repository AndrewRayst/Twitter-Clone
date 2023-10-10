import os

from dotenv import load_dotenv

load_dotenv()

LOADING_IMAGE_SRC: str = os.getenv(
    "", "http://localhost:5000/static/images/loading.gif"
)
