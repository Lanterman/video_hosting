import datetime

from pydantic import BaseModel

from user.schemas import User


class Video(BaseModel):
    name: str
    description: str
    path_to_file: str
    date_of_creation: datetime.datetime


class GetVideoList(Video):
    user: User


class CreateVideo(GetVideoList):
    pass
