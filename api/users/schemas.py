import datetime
from pydantic import BaseModel, EmailStr, Field


class SUser(BaseModel):
    id: int
    username: str = Field(max_length=90)
    password: str
    email: EmailStr
    birthday: datetime.date   
    bio: str
