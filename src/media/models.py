from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, MappedColumn

from src.database.models import BaseModel
from src.tweets.models import TweetModel


class MediaModel(BaseModel):
    __tablename__ = "media"
    tweet_id: Mapped[int] = MappedColumn(Integer(), ForeignKey(TweetModel.id), nullable=True)
    src: Mapped[str]
