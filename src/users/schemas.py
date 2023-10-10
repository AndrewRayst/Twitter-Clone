from typing import Optional

from pydantic import BaseModel

from src.schemas import SuccessResponseSchema


class UserSchema(BaseModel):
    id: Optional[int]
    name: str

    class ConfigDict:
        from_attributes = True


class UserOutSchema(UserSchema):
    followers: list[UserSchema]
    following: list[UserSchema]


class SuccessResponseUserSchema(SuccessResponseSchema):
    user: UserOutSchema
