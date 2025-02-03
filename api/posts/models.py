import datetime
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey, String, Text, func
from users.models import User
from database import Model


class Post(Model):
    __tablename__ = "post"

    title: Mapped[str] = mapped_column(String(length=127), unique=True, nullable=False)
    text: Mapped[str] = mapped_column(Text(), nullable=True)
    created_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    update_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    author: Mapped["User"] = mapped_column(ForeignKey("user.id", ondelete="cascade"))

    users: Mapped[List["User"]] = relationship(back_populates="posts")
