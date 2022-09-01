from scr.user import services
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/auth")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    token = await services.get_user_token(token)

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticated": "Bearer"}
        )
    if not token.user_id.is_activate:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user!")
    return token.user_id
