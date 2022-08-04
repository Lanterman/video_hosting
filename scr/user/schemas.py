import datetime

from typing import Optional
from pydantic import BaseModel, EmailStr, validator
from pydantic.fields import Field
from pydantic.types import UUID4

from scr.video.models import Video


class UserBase(BaseModel):
    username: str
    phone: str
    email: EmailStr


class GetUserBase(UserBase):
    video_set: list[Video]


class UserCreate(UserBase):
    password: str


class TokenBase(BaseModel):
    token: UUID4 = Field(..., alias="access_token")
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
