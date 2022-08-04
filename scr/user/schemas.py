import datetime

from typing import Optional
from pydantic import UUID4, BaseModel, EmailStr, Field, validator

from scr.video.models import Video


class UserBase(BaseModel):
    username: str
    phone: str
    email: EmailStr


class   GetUserBase(UserBase):
    video_set: list[Video]


class UserCreate(UserBase):
    password: str


class TokenBase(BaseModel):
    expires: datetime.datetime
    token_type: Optional[str] = "Bearer"

    class Config:
        allow_population_by_field_name = True

    @classmethod
    @validator("token")
    def hexlify_token(cls, value):
        return value.hex


class User(UserBase):
    token: TokenBase = {}
