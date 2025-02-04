import datetime
from pydantic import BaseModel, EmailStr, Field


class SUserView(BaseModel):
    id: int
    username: str = Field(max_length=90)
    birthday: datetime.date   
    bio: str


class SUser(SUserView):
    password: str
    email: EmailStr
