from typing import Optional

from pydantic import BaseModel

from src.schemas import SuccessResponseSchema
from src.users.schemas import UserSchema


class TweetSchema(BaseModel):
    tweet_data: str
    tweet_media_ids: Optional[list[int]]


class SuccessTweetPostResponseSchema(SuccessResponseSchema):
    tweet_id: int


class SuccessTweetGetResponseSchema:
    tweet_id: int
    content: str
    attachments: list[str]
    author: UserSchema
    likes: list[UserSchema]


class SuccessTweetsResponseSchema(SuccessResponseSchema):
    tweets: list[SuccessTweetGetResponseSchema]
