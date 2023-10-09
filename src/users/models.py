from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, MappedColumn, relationship

from src.database.models import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"
    name: Mapped[str] = MappedColumn(String(length=50))
    api_key_hash: Mapped[str]

    followers: Mapped[list["UserFollowerModel"]] = relationship(
        "UserFollowerModel",
        primaryjoin="UserFollowerModel.user_id == UserModel.id",
        lazy="joined",
    )

    following: Mapped[list["UserFollowerModel"]] = relationship(
        "UserFollowerModel",
        primaryjoin="UserFollowerModel.follower_id == UserModel.id",
        lazy="joined",
    )


class UserFollowerModel(BaseModel):
    __tablename__ = "user_followers"
    __table_args__ = (
        UniqueConstraint("user_id", "follower_id", name="unique_follower_id"),
    )
    user_id: Mapped[int] = MappedColumn(
        Integer(), ForeignKey("users.id", ondelete="CASCADE")
    )
    follower_id: Mapped[int] = MappedColumn(
        Integer(), ForeignKey("users.id", ondelete="CASCADE")
    )
