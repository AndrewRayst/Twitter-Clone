from typing import Optional

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: Optional[int]

    class Config:
        orm_mode = True


class UserOutSchema(UserSchema):
    followers: list[UserSchema]
    following: list[UserSchema]
