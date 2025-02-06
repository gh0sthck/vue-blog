import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, Text, func, ForeignKey, Integer, Column, Table

from database import Model
from users.models import User


class Review(Model):
    __tablename__ = "review"

    text: Mapped[str] = mapped_column(Text(), nullable=True)
    author: Mapped["User"] = mapped_column(ForeignKey("user.id", ondelete="cascade"))
    create_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(), server_default=func.now()
    )


Comment = Table(
    "comment",
    Model.metadata,
    Column("id", Integer(), primary_key=True, autoincrement=True, unique=True),
    Column("post_id", ForeignKey("post.id", ondelete="cascade")),
    Column("review_id", ForeignKey("review.id", ondelete="cascade")),
)
