from fastapi import Request, APIRouter, WebSocket, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from config.dependecies import get_current_user
from config.utils import http404_error_handler
from scr.user.models import Users
from scr.video.services import set_like
from scr.video.models import Video

html_router = APIRouter(prefix="/html", tags=["html"])
templates = Jinja2Templates(directory="templates")


@html_router.get("/watch/{video_id}", response_class=HTMLResponse, include_in_schema=False)
async def set_like_html(request: Request, video_id: int):
    video = await http404_error_handler(class_model=Video, attribute=video_id)
    count_likes = await video.like_users.count()
    context = {"request": request, "path": video_id, "count_likes": count_likes}
    return templates.TemplateResponse("watch_video.html", context)


@html_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, current_user: Users = Depends(get_current_user)):
    await websocket.accept()
    while True:
        data = await websocket.receive()
        count_likes = await set_like(data["text"], current_user)
        await websocket.send_text(f"{count_likes}")
