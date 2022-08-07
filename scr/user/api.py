from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic.networks import EmailStr

from config.utils import http404_error_handler
from scr.user import services
from .models import Users
from .schemas import GetUserBase, User as UserSchema, UserCreate, TokenBase, UserBase, UserUpdate
from .dependecies import get_current_user


user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get("/channel/{username}", response_model=GetUserBase, description="User video list")
async def get_user_video(username: str):
    user = await http404_error_handler(Users, username)
    return user


@user_router.post("/sign-up", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    db_user = await services.get_user_by_username(username=user.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered!")
    return await services.create_user(user=user)


@user_router.post("/auth", response_model=TokenBase)
async def auth(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await services.get_user_by_username(username=form_data.username)

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password!")

    if not services.validate_password(password=form_data.password, hashed_password=user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password!")

    return await services.create_user_token(user_id=user.id)


@user_router.get("/me", response_model=UserBase, description="Get user")
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user


@user_router.put(
    "/update_info", response_model=UserUpdate, status_code=status.HTTP_201_CREATED, description="Update user"
)
async def update_user(username: str, phone: int, email: EmailStr, current_user: Users = Depends(get_current_user)):
    user = await services.update_user_info(username=username, phone=phone, email=email, user=current_user)
    return user


@user_router.put("/reset_password", description="Reset user password")
async def reset_password(password1: str, password2: str, current_user: Users = Depends(get_current_user)):
    await services.reset_password(password1=password1, password2=password2, user=current_user)
    return {"Detail": "Successful!", "user": current_user}


@user_router.delete("/delete_user", description="Delete user")
async def delete_user(current_user: Users = Depends(get_current_user)):
    result = await services.delete_user(user=current_user)
    return {"Detail": "Successful!", "user": result}
