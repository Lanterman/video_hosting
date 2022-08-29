from fastapi import Request, APIRouter, WebSocket, HTTPException, status, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from config.dependecies import get_current_user
from scr.user import services
from scr.user.models import Users


html_user_router = APIRouter(prefix="/html", tags=["html"])
templates = Jinja2Templates(directory="templates")


@html_user_router.get("/channel/{username}", response_class=HTMLResponse, include_in_schema=False)
async def set_like_html(request: Request, username: str, current_user: Users = Depends(get_current_user)):
    user_videos = await services.get_user_and_his_video_by_username(username=username)

    if not user_videos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")

    subscribers = await services.get_user_subscribers(username)

    context = {"request": request, "subscribers": len(subscribers),
               "user": user_videos, "current_user": current_user.username}
    return templates.TemplateResponse("user_channel.html", context)


@html_user_router.websocket("/ws/channel")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    owner, current_user = None, None

    while True:
        data = await websocket.receive_text()
        data = data.split(", ")

        if not owner:
            owner = await services.get_user_by_username(username=data[0])

        if not current_user:
            current_user = await services.get_user_by_username(username=data[1])

        subscribers = await services.follow_or_unfollow(owner=owner, subscriber=current_user)
        subscribers = str(len(subscribers))
        await websocket.send_text(subscribers)
