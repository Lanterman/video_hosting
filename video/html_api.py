from fastapi import Request, APIRouter, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from config.utils import http404_error_handler
from video.services import set_like
from video.models import Video

html_router = APIRouter(prefix="/html", tags=["html"])
templates = Jinja2Templates(directory="templates")


@html_router.get("/watch/{video_id}", response_class=HTMLResponse, include_in_schema=False)
async def set_like_html(request: Request, video_id: int):
    video = await http404_error_handler(class_model=Video, attribute=video_id, video=True)
    count_likes = await video.like_users.count()
    context = {"request": request, "path": video_id, "count_likes": count_likes}
    return templates.TemplateResponse("watch_video.html", context)


@html_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive()
        count_likes = await set_like(data["text"])
        await websocket.send_text(f"{count_likes}")
