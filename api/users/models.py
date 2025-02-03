import datetime
import typing
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Date

from database import Model

if typing.TYPE_CHECKING:
    from api.posts.models import Post


class User(Model):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(
        String(length=90), unique=True, nullable=False
    )
    email: Mapped[str] = mapped_column(String(), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    bio: Mapped[str]
    birthday: Mapped[datetime.date] = mapped_column(Date())
    posts: Mapped[typing.List["Post"]] = relationship(back_populates="users")
