from pydantic import BaseModel

from video.models import Video


class User(BaseModel):
    username: str
    phone: str
    email: str


class GetUser(User):
    video_set: list[Video]
