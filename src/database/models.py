from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedColumn


class BaseModel(DeclarativeBase):
    id: Mapped[int] = MappedColumn(Integer(), primary_key=True)
