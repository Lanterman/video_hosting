import ormar

import datetime
from typing import Optional

from config.utils import MainMeta
from scr.user.models import Users


class Video(ormar.Model):
    class Meta(MainMeta):
        tablename = "video"

    id: int = ormar.Integer(primary_key=True, index=True)
    name: str = ormar.String(max_length=50)
    description: str = ormar.String(max_length=500)
    path_to_file: str = ormar.String(max_length=1000, unique=True)
    date_of_creation: datetime.datetime = ormar.DateTime(default=datetime.datetime.now)
    user: Optional[Users] = ormar.ForeignKey(to=Users, related_name="video_set", ondelete="CASCADE")
    like_users: Optional[list[Users]] = ormar.ManyToMany(to=Users, related_name="user_likes")
