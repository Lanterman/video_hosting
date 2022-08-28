from fastapi import Request, APIRouter, WebSocket, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from config.dependecies import get_current_user
from scr.user import services
from scr.user.models import Users


html_user_router = APIRouter(prefix="/html", tags=["html"])
templates = Jinja2Templates(directory="templates")


@html_user_router.get("/channel/{username}", response_class=HTMLResponse, include_in_schema=False)
async def set_like_html(request: Request, username: str):
    user_videos = await services.get_user_and_his_video_by_username(username=username)

    if not user_videos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")

    subscribers = await services.get_user_subscribers(username)

    context = {"request": request, "subscribers": len(subscribers), "user": user_videos}
    return templates.TemplateResponse("user_channel.html", context)


@html_user_router.websocket("/ws/channel")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        # current_user: Users | None = await get_current_user()
        current_user: Users = await Users.objects.get(username="lanterman")
    except HTTPException:
        await websocket.send_text("Not authorization!")
    else:
        user = None
        while True:
            data = await websocket.receive()

            if not user:
                user = await services.get_user_by_username(username=data["text"])

                if not user:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")

                if user.id == current_user.id:
                    raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Can't follow yourself!")

            subscribers = await services.follow_or_unfollow(owner=user, subscriber=current_user)
            subscribers = str(len(subscribers))
            await websocket.send_text(subscribers)
