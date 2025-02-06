import datetime
from pydantic import BaseModel, Field


class SPost(BaseModel):
    title: str = Field(max_length=127)
    text: str
    author: int


class SPostService(SPost):
    id: int
    created_date: datetime.datetime
    update_date: datetime.datetime


class SPostTest(SPost):
    id: int
