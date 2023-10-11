from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, MappedColumn, relationship

from src.database.models import BaseModel
from src.users.models import UserModel


class TweetModel(BaseModel):
    __tablename__ = "tweets"

    user_id: Mapped[int] = MappedColumn(
        Integer(), ForeignKey(UserModel.id, ondelete="CASCADE")
    )
    content: Mapped[str]

    media_ids: Mapped[list[int]] = relationship(
        argument="MediaModel",
        primaryjoin="TweetModel.id == MediaModel.tweet_id",
        lazy="joined",
    )
    #
    # author: Mapped[list[int]] = relationship(
    #     argument="UserModel",
    #     primaryjoin="TweetModel.user_id == UserModel.id",
    #     lazy="joined",
    # )
