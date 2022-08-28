import datetime
import re

from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr
from pydantic import validator
from pydantic.fields import Field
from pydantic.types import UUID4

from scr.video.models import Video


class UserBase(BaseModel):
    """Base user schema"""

    id: int
    username: str
    phone: int
    email: EmailStr


class SubscriberBase(BaseModel):
    """Base subscriber"""

    subscriber: UserBase


class GetUserVideo(UserBase):
    """User video get schema - response model"""

    video_set: list[Video]
    subscribers: list[SubscriberBase]


class ResetPassword(BaseModel):
    """User password reset schema - path arguments and fields validation"""

    old_password: str
    password1: str
    password2: str

    @validator("password1")
    def compare_old_and_new_passwords(cls, password1, values):
        if values["old_password"] == password1:
            raise HTTPException(status_code=406, detail="New password and old password can't match!")
        return password1

    @validator("password1")
    def len_password1(cls, password1):
        if len(password1) < 10:
            raise HTTPException(status_code=406, detail="Too small password field! Minimum length 10 characters!")
        return password1

    @validator("password2")
    def compare_password1_and_password2(cls, password2, values):
        if values["password1"] != password2:
            raise HTTPException(status_code=406, detail="Passwords don't match!")
        return password2


class UserUpdate(UserBase):
    """User update schema - response model, path arguments and fields validation"""

    @validator("username")
    def len_username(cls, value):
        if len(value) < 5:
            raise HTTPException(status_code=406, detail="Too small username field! Minimum length 5 characters!")
        return value

    @validator("username")
    def first_character_is_number(cls, value):
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
    """User creation schema - path arguments and fields validation"""

    password: str

    @validator("password")
    def len_password1(cls, password):
        if len(password) < 10:
            raise HTTPException(status_code=406, detail="Too small password field! Minimum length 10 characters!")
        return password


class TokenBase(BaseModel):
    """Scheme for creating a token - authentication, response model"""

    token: UUID4 = Field(..., alias="access_token")
    expires: datetime.datetime
    token_type: Optional[str] = "Bearer"

    class Config:
        allow_population_by_field_name = True


class UserSchema(UserBase):
    """User creation schema - response model"""

    token: TokenBase = {}


class Subscriber(BaseModel):
    """Base subscriber schema"""

    owner: UserBase
    subscriber: UserBase
