from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from config.utils import http404_error_handler
from scr.user import services
from .models import Users
from .schemas import UserCreate, TokenBase, UserBase, UserUpdate, GetUserVideo, ResetPassword, User as UserSchema
from .dependecies import get_current_user


user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get("/channel/{username}", response_model=GetUserVideo, description="User video list")
async def get_user_video(username: str):
    """Get user videos - endpoint"""

    user_videos = await http404_error_handler(Users, username)
    return user_videos


@user_router.post("/sign-up", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """Create user - endpoint"""

    db_user = await services.get_user_by_username(username=user.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered!")

    db_user = await services.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with that email already registered!")

    return await services.create_user(user=user)


@user_router.post("/auth", response_model=TokenBase, include_in_schema=False)
async def auth(form_data: OAuth2PasswordRequestForm = Depends()):
    """User authentication - endpoint"""

    user = await services.get_user_by_username(username=form_data.username)

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password!")

    if not services.validate_password(password=form_data.password, hashed_password=user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password!")

    return await services.create_user_token(user_id=user.id)


@user_router.get("/me", response_model=UserBase, description="Get user")
async def get_user(current_user: Users = Depends(get_current_user)):
    """Get user - endpoint"""

    return current_user


@user_router.put(
    "/update_info", response_model=UserUpdate, status_code=status.HTTP_201_CREATED, description="Update user"
)
async def update_user(update_data: UserUpdate, current_user: Users = Depends(get_current_user)):
    """Update user information - endpoint"""

    db_user = await services.get_user_by_email(email=update_data.email)
    if db_user and db_user != current_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with that email already registered!")

    user = await services.update_user_info(
        username=update_data.username, phone=update_data.phone, email=update_data.email, user=current_user
    )
    return user


@user_router.put("/reset_password", description="Reset user password")
async def reset_password(reset_data: ResetPassword, current_user: Users = Depends(get_current_user)):
    """Reset user password - endpoint"""

    if not services.validate_password(password=reset_data.old_password, hashed_password=current_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong old password!")

    await services.reset_password(new_password=reset_data.password1, user=current_user)
    return {"Detail": "Successful!", "user": current_user}


@user_router.delete("/delete_user", description="Delete user")
async def delete_user(current_user: Users = Depends(get_current_user)):
    """Delete user - endpoint"""

    result = await services.delete_user(user=current_user)
    return {"Detail": "Successful!", "user": result}
