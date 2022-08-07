import datetime
import re

from typing import Optional

from fastapi import HTTPException
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


class ResetPassword(BaseModel):
    password1: str
    password2: str

    @validator("password1")
    def len_username(cls, value):
        if len(value) < 10:
            raise HTTPException(status_code=406, detail="Too small password field! Minimum length 10 characters!")
        return value


class UserUpdate(UserBase):
    pass

    @validator("username")
    def len_username(cls, value):
        if len(value) < 5:
            raise HTTPException(status_code=406, detail="Too small username field! Minimum length 5 characters!")
        return value

    @validator("username")
    def first_character_is_number(cls, value):
        print(re.match(r"\d", value))
        if re.match(r"\d", value):
            raise HTTPException(status_code=406, detail="First character can not be number!")
        return value

    @validator("email")
    def len_email(cls, value):
        email = re.split("@", value)
        if len(email[0]) < 5:
            raise HTTPException(status_code=406, detail="Too small email field! Minimum length 5 characters before @!")
        return value


class UserCreate(UserUpdate):
    password: str

    @validator("password")
    def len_username(cls, value):
        if len(value) < 10:
            raise HTTPException(status_code=406, detail="Too small password field! Minimum length 10 characters!")
        return value


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
