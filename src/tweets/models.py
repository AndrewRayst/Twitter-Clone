from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, MappedColumn, relationship

from src.database.models import BaseModel
from src.media.models import MediaModel
from src.users.models import UserModel


class TweetModel(BaseModel):
    __tablename__ = "tweets"

    user_id: Mapped[int] = MappedColumn(
        Integer(), ForeignKey(UserModel.id, ondelete="CASCADE")
    )
    content: Mapped[str]

    media: Mapped[list[MediaModel]] = relationship(
        argument=MediaModel,
        primaryjoin="TweetModel.id == MediaModel.tweet_id",
        lazy="joined",
    )

    author: Mapped[UserModel] = relationship(
        argument="UserModel",
        primaryjoin="TweetModel.user_id == UserModel.id",
        lazy="joined",
    )

    likes: Mapped[list[UserModel]] = relationship(
        argument="UserModel",
        secondary="tweet_likes",
        primaryjoin="TweetModel.id == TweetLikeModel.tweet_id",
        secondaryjoin="TweetLikeModel.user_id == UserModel.id",
        lazy="joined",
    )


class TweetLikeModel(BaseModel):
    __tablename__ = "tweet_likes"
    __table_args__ = (
        UniqueConstraint("tweet_id", "user_id", name="unique_tweet_like_id"),
    )
    tweet_id: Mapped[int] = MappedColumn(
        Integer(), ForeignKey("tweets.id", ondelete="CASCADE")
    )
    user_id: Mapped[int] = MappedColumn(
        Integer(), ForeignKey("users.id", ondelete="CASCADE")
    )
