import datetime
from pydantic import BaseModel, Field


class SPost(BaseModel):
    id: int
    title: str = Field(max_length=127)
    text: str
    author: int


class SPostService(SPost):
    title: str = Field(max_length=127)
    text: str 
    author: int 
    created_date: datetime.datetime | None = None
    update_date: datetime.datetime | None = None
