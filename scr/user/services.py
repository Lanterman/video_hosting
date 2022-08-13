import hashlib
import random
import uuid
import string
import os
import shutil

from datetime import datetime, timedelta

from fastapi import BackgroundTasks
from pydantic.networks import EmailStr

from config.utils import BASE_DIR
from scr.user.models import Users, Tokens
from scr.user.schemas import UserCreate


def get_random_string(length=12):
    """Generate random string to use as salt"""

    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def hash_password(password: str, salt: str = None):
    """Hash password with salt"""

    if salt is None:
        salt = get_random_string()
    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return enc.hex()


def validate_password(password: str, hashed_password: str):
    """Check if password matches hash from database"""

    salt, hashed = hashed_password.split("$")
    return hash_password(password, salt) == hashed


async def get_user_and_his_video_by_username(username: str):
    """Return user information and his video by the username"""

    query = await Users.objects.select_related("video_set").all(username=username)
    return query[0] if query else query


async def get_user_by_username(username: str):
    """Return user information by the username"""

    query = await Users.objects.all(username=username)
    return query[0] if query else query


async def get_user_by_email(email: EmailStr):
    """Return user information by the username"""

    query = await Users.objects.all(email=email)
    return query[0] if query else query


async def get_user_by_token(token: str):
    """Return information about owner of specified token"""

    query = await Tokens.objects.select_related("user_id").all(token=token, expires__gt=datetime.now())
    return query[0] if query else query


async def create_user_token(user_id: int):
    """Create token for user of specified user_id"""

    my_uuid = uuid.uuid4()
    await Tokens.objects.delete(user_id=user_id)
    query = await Tokens.objects.create(expires=datetime.now() + timedelta(weeks=2), user_id=user_id, token=my_uuid)
    return query


def create_user_directory(user_id):
    """Create custom directory for user video"""

    if str(user_id) not in os.listdir(path=f"{BASE_DIR}/uploaded_files"):
        os.mkdir(path=f"{BASE_DIR}/uploaded_files/{user_id}")


def delete_user_directory(user_id):
    """Delete custom directory for user video"""

    if str(user_id) in os.listdir(path=f"{BASE_DIR}/uploaded_files"):
        shutil.rmtree(path=f"{BASE_DIR}/uploaded_files/{user_id}")


async def create_user(user: UserCreate, background_task: BackgroundTasks):
    """Create new user in database"""

    salt = get_random_string()
    hashed_password = hash_password(user.password, salt)
    new_user = await Users.objects.create(
        username=user.username, email=user.email, phone=user.phone, hashed_password=f"{salt}${hashed_password}"
    )
    background_task.add_task(create_user_directory, new_user.id)
    token = await create_user_token(new_user)
    token_dict = {"token": token.token, "expires": token.expires}

    return {**user.dict(), "id": new_user.id, "is_activate": True, "token": token_dict}


async def update_user_info(username: str, phone: int, email: EmailStr, user: Users):
    """Update user information"""

    await user.update(username=username, phone=phone, email=email)
    return user


async def reset_password(new_password: str, user: Users) -> None:
    """Reset user password"""

    salt = get_random_string()
    hashed_password = hash_password(new_password, salt)
    await user.update(hashed_password=f"{salt}${hashed_password}")


async def delete_user(user: Users, background_task: BackgroundTasks):
    """Delete user"""

    await user.delete()
    background_task.add_task(delete_user_directory, user.id)
    return user.id
