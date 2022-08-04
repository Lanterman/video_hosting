from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from config.utils import http404_error_handler
from scr.user import services
from .models import Users
from .schemas import GetUserBase, User as UserSchema, UserCreate, TokenBase, UserBase
from .dependecies import get_current_user


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


@user_router.post("/auth", response_model=TokenBase)
async def auth(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await services.get_user_by_email(email=form_data.username)

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password!")

    if not services.validate_password(password=form_data.password, hashed_password=user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password!")

    return await services.create_user_token(user_id=user.id)


@user_router.get("/me", response_model=UserBase)
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user.user_id
