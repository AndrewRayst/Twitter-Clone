from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, MappedColumn

from src.database.models import BaseModel


class MediaModel(BaseModel):
    __tablename__ = "media"
    tweet_id: Mapped[int] = MappedColumn(
        Integer(), ForeignKey("tweets.id"), nullable=True
    )
    src: Mapped[str]
