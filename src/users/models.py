from sqlalchemy import String
from sqlalchemy.orm import Mapped, MappedColumn

from src.database.models import PrimaryKeyModel


class UserModel(PrimaryKeyModel):
    __tablename__ = "users"
    name: Mapped[str] = MappedColumn(String(length=50))
    api_key_hash: Mapped[str]
