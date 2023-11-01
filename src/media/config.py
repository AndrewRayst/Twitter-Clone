import os

from dotenv import load_dotenv

load_dotenv()

LOADING_IMAGE_SRC: str = os.getenv(
    "LOADING_IMAGE", "http://localhost:5000/static/images/loading.gif"
)

YANDEX_S3_BUCKET_NAME: str = os.getenv("YANDEX_S3_BUCKET_NAME", "")
YANDEX_S3_IMAGES_URL: str = os.getenv("YANDEX_S3_IMAGES_URL", "")
