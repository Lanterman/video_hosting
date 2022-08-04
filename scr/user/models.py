import ormar
import datetime

from pydantic.types import UUID4

from config.utils import MainMeta


class Users(ormar.Model):
    class Meta(MainMeta):
        tablename = "users"

    id: int = ormar.Integer(primary_key=True)
    username: str = ormar.String(max_length=100, unique=True)
    phone: int = ormar.String(max_length=14, unique=True)
    email = ormar.String(index=True, unique=True, max_length=255)
    hashed_password = ormar.String(max_length=300)
    is_activate = ormar.Boolean(default=True)
    is_superuser = ormar.Boolean(default=False)


class Tokens(ormar.Model):
    class Meta(MainMeta):
        tablename = "tokens"

    id: int = ormar.Integer(primary_key=True)
    token: UUID4 = ormar.String(index=True, unique=True, max_length=255)
    expires: datetime.datetime = ormar.DateTime()
    user_id: int = ormar.ForeignKey(Users)
