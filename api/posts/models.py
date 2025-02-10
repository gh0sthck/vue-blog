import datetime
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, Text, func
from comments.models import Comment, Review
from users.models import User
from database import Model


class Post(Model):
    __tablename__ = "post"

    title: Mapped[str] = mapped_column(String(length=127), unique=True, nullable=False)
    text: Mapped[str] = mapped_column(Text(), nullable=True)
    created_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(), server_default=func.now()
    )
    update_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(), server_default=func.now(), onupdate=func.now()
    )
    author: Mapped["User"] = mapped_column(ForeignKey("user.id", ondelete="cascade"))

    users: Mapped[List["User"]] = relationship(back_populates="posts")
    reviews: Mapped[list["Review"]] = relationship(backref="posts", secondary=Comment)


Like = Table(
    "like",
    Model.metadata,
    Column("id", Integer(), primary_key=True, autoincrement=True),
    Column("post_id", ForeignKey("post.id", ondelete="cascade")),
    Column("user_id", ForeignKey("user.id", ondelete="cascade")),
)
