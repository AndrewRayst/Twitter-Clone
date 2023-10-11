from typing import Optional

from pydantic import BaseModel

from src.schemas import SuccessResponseSchema


class TweetSchema(BaseModel):
    tweet_data: str
    tweet_media_ids: Optional[list[int]]


class SuccessTweetResponseSchema(SuccessResponseSchema):
    tweet_id: int
