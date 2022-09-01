from fastapi import Request, APIRouter, WebSocket, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from config.dependecies import get_current_user
from config.utils import http404_error_handler

from scr.user import models, services
from scr.video.services import set_like
from scr.video.models import Video

html_video_router = APIRouter(prefix="/html", tags=["html"])
templates = Jinja2Templates(directory="templates")


@html_video_router.get("/watch/{video_id}", response_class=HTMLResponse, include_in_schema=False)
async def set_like_html(request: Request, video_id: int, current_user: models.Users = Depends(get_current_user)):
    video = await http404_error_handler(class_model=Video, attribute=video_id)
    count_likes = await video.like_users.count()
    context = {"request": request, "video_id": video_id, "count_likes": count_likes,
               "current_user": current_user.username}
    return templates.TemplateResponse("watch_video.html", context)


@html_video_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    current_user = None

    while True:
        data = await websocket.receive_text()
        video_id, username = data.split(", ")

        if not current_user:
            current_user = await services.get_user_by_username(username)

        count_likes = await set_like(int(video_id), current_user)
        await websocket.send_text(f"{count_likes}")
