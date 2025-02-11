import datetime
from pydantic import BaseModel, EmailStr, Field

from settings import config


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


class SJWTPayload(BaseModel):
    username: str
    email: EmailStr
    expire: int = (datetime.datetime.now() + datetime.timedelta(minutes=config.auth.ACCESS_TOKEN_EXPIRE_MIN)).minute


class SJWTToken(BaseModel):
    token: bytes
    access_type: str = "Bearer"
