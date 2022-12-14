import ormar
import datetime

from pydantic.types import UUID4
from pydantic import EmailStr

from config.utils import MainMeta


class Users(ormar.Model):
    class Meta(MainMeta):
        tablename = "users"

    id: int = ormar.Integer(primary_key=True)
    username: str = ormar.String(index=True, max_length=100, unique=True)
    phone: str = ormar.String(max_length=14, default="0")
    email: EmailStr = ormar.String(index=True, unique=True, max_length=255)
    hashed_password: str = ormar.String(max_length=300)
    is_activate: bool = ormar.Boolean(default=True)
    is_superuser: bool = ormar.Boolean(default=False)


class Tokens(ormar.Model):
    class Meta(MainMeta):
        tablename = "tokens"

    id: int = ormar.Integer(primary_key=True)
    token: UUID4 = ormar.UUID(index=True, unique=True, uuid_format="string")
    expires: datetime.datetime = ormar.DateTime()
    user_id: int = ormar.ForeignKey(Users, ondelete="CASCADE")


class Subscriber(ormar.Model):
    class Meta(MainMeta):
        tablename = "subscribers"

    id: int = ormar.Integer(primary_key=True)
    owner: int = ormar.ForeignKey(to=Users, ondelete="CASCADE", nullable=False)
    subscriber: int = ormar.ForeignKey(to=Users, ondelete="CASCADE", related_name="subscribers", nullable=False)
