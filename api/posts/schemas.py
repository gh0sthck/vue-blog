import datetime
from pydantic import BaseModel, Field


class SPost(BaseModel):
    title: str = Field(max_length=127)
    text: str
    author: int | None = None


class SPostService(SPost):
    id: int
    created_date: datetime.datetime
    update_date: datetime.datetime


class SPostTest(SPost):
    id: int


class SLike(BaseModel):
    user_id: int
    post_id: int


class SLikeService(SLike):
    id: int
