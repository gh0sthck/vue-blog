import datetime
from pydantic import BaseModel, Field


class SPostInsert(BaseModel):
    id: int
    title: str = Field(max_length=127)
    text: str
    author: int


class SPost(SPostInsert):
    created_date: datetime.datetime | None = None
    update_date: datetime.datetime | None = None
