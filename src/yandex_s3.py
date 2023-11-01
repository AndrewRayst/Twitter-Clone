import boto3

from src import config

session = boto3.session.Session(
    aws_access_key_id=config.YANDEX_S3_ACCESS_KEY_ID,
    aws_secret_access_key=config.YANDEX_S3_SECRET_ACCESS_KEY,
    region_name=config.YANDEX_S3_REGION_NAME,
)
