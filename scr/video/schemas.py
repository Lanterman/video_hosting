import datetime

from pydantic import BaseModel

from scr.user.schemas import UserBase


class Video(BaseModel):
    name: str
    description: str
    path_to_file: str
    date_of_creation: datetime.datetime


class GetVideoList(Video):
    user: UserBase


class CreateVideo(GetVideoList):
    pass
