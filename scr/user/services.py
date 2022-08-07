import hashlib
import random
import uuid
import string
from datetime import datetime, timedelta

from fastapi import HTTPException
from pydantic.networks import EmailStr

from scr.user.models import Users, Tokens
from scr.user.schemas import UserCreate, ResetPassword


def get_random_string(length=12):
    """ Генерирует случайную строку, использующуюся как соль """
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def hash_password(password: str, salt: str = None):
    """ Хеширует пароль с солью """
    if salt is None:
        salt = get_random_string()
    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return enc.hex()


def validate_password(password: str, hashed_password: str):
    """ Проверяет, что хеш пароля совпадает с хешем из БД """
    salt, hashed = hashed_password.split("$")
    return hash_password(password, salt) == hashed


async def get_user_by_username(username: str):
    """ Возвращает информацию о пользователе """
    query = await Users.objects.all(username=username)
    return query[0] if query else query


async def get_user_by_token(token: str):
    """ Возвращает информацию о владельце указанного токена """
    query = await Tokens.objects.select_related("user_id").all(token=token, expires__gt=datetime.now())
    return query[0] if query else query


async def create_user_token(user_id: int):
    """ Создает токен для пользователя с указанным user_id """
    my_uuid = uuid.uuid4()
    query = await Tokens.objects.create(expires=datetime.now() + timedelta(weeks=2), user_id=user_id, token=my_uuid)
    return query


async def create_user(user: UserCreate):
    """ Создает нового пользователя в БД """
    salt = get_random_string()
    hashed_password = hash_password(user.password, salt)
    user_id = await Users.objects.create(username=user.username, email=user.email, phone=user.phone,
                                         hashed_password=f"{salt}${hashed_password}")
    token = await create_user_token(user_id)
    token_dict = {"token": token.token, "expires": token.expires}

    return {**user.dict(), "id": user_id, "is_activate": True, "token": token_dict}


async def update_user_info(username: str, phone: int, email: EmailStr, user: Users):
    """Обновление данных пользователя"""
    await user.update(username=username, phone=phone, email=email)
    return user


async def reset_password(password1: str, password2: str, user: Users) -> None:
    """Сброс пароля"""
    if password1 != password2:
        raise HTTPException(status_code=406, detail="Passwords don't match!")
    ResetPassword(password1=password1, password2=password2)
    salt = get_random_string()
    hashed_password = hash_password(password1, salt)
    await user.update(hashed_password=hashed_password)


async def delete_user(user: Users):
    """Удалить пользователя"""
    print(user)
    user = await Users.objects.delete(id=user.id)
    return user
