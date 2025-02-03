import datetime
from pydantic import BaseModel, Field


class SPost(BaseModel):
    id: int
    title: str = Field(max_length=127)
    text: str
    created_date: datetime.datetime
    update_date: datetime.datetime
