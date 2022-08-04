from scr.user import services
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/auth")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = await services.get_user_by_token(token)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticated": "Bearer"}
        )
    if not user.user_id.is_activate:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user!")
    return user
