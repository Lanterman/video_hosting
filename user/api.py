from fastapi import APIRouter

from config.utils import http404_error_handler
from .models import User
from .schemas import GetUser


user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get("/channel/{username}", response_model=GetUser, description="User video list")
async def get_user_video(username: str):
    user = await http404_error_handler(User, username)
    return user
