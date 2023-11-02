from typing import Optional

from pydantic import BaseModel, Field

from src.schemas import SuccessResponseSchema
from src.users.schemas import UserSchema


class TweetSchema(BaseModel):
    tweet_data: str
    tweet_media_ids: Optional[list[int]]


class SuccessTweetPostResponseSchema(SuccessResponseSchema):
    tweet_id: int


class TweetUserLikeSchema(UserSchema):
    id: int = Field(serialization_alias="user_id")


class SuccessTweetGetResponseSchema(BaseModel):
    id: int
    content: str
    attachments: list[str]
    author: UserSchema
    likes: list[TweetUserLikeSchema]


class SuccessTweetsResponseSchema(SuccessResponseSchema):
    tweets: list[SuccessTweetGetResponseSchema]
