import datetime
from pydantic import BaseModel, EmailStr, Field


class SUserView(BaseModel):
    username: str = Field(max_length=90)
    birthday: datetime.date
    bio: str


class SUser(SUserView):
    password: str
    email: EmailStr


class SUserService(SUserView):
    id: int


class SUserTest(SUser):
    id: int
