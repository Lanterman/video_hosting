import ormar

from config.utils import MainMeta


class User(ormar.Model):
    class Meta(MainMeta):
        tablename = "user"

    id: int = ormar.Integer(primary_key=True)
    username: str = ormar.String(max_length=100, unique=True)
    phone: str = ormar.String(max_length=14, unique=True)
    email = ormar.String(index=True, unique=True, max_length=255)
    is_activate = ormar.Boolean(default=True)
    is_superuser = ormar.Boolean(default=False)
