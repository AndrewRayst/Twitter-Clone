from sqlalchemy.orm import Mapped

from src.database.models import BaseModel


class MediaModel(BaseModel):
    __tablename__ = "media"
    src: Mapped[str]
