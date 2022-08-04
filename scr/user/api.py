from fastapi import APIRouter, HTTPException, status

from config.utils import http404_error_handler
from .models import Users
from .schemas import GetUserBase, User as UserSchema, UserCreate
from scr.user import services


user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get("/channel/{username}", response_model=GetUserBase, description="User video list")
async def get_user_video(username: str):
    user = await http404_error_handler(Users, username)
    return user


@user_router.post("/sign-up", response_model=UserSchema)
async def create_user(user: UserCreate):
    db_user = await services.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered!")
    return await services.create_user(user=user)
