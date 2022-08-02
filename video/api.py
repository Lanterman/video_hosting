from fastapi import APIRouter, Form, File, UploadFile
from fastapi.responses import StreamingResponse

from config.utils import http404_error_handler
from user.models import User
from .models import Video
from .schemas import CreateVideo, GetVideoList
from .services import save_video, set_like


video_router = APIRouter(prefix="/video", tags=["video"])


@video_router.get("/", response_model=list[GetVideoList], description="Video list output")
async def get_video_list():
    list_video = await Video.objects.select_related("user").all()
    return list_video


@video_router.post("/create_video", response_model=CreateVideo, status_code=201, description="Download video file")
async def create_video(name: str = Form(), description: str = Form(), file: UploadFile = File()):
    user = await User.objects.first()
    return await save_video(name=name, description=description, file=file, user=user)


@video_router.get("/watch/{video_id}", description="Watch streaming video")
async def get_video(video_id: int):
    video = await http404_error_handler(class_model=Video, attribute=video_id, video=True)
    open_video = open(video.path_to_file, "rb")
    media_type = f"video/{video.path_to_file[-3:]}"
    return StreamingResponse(open_video, media_type=media_type)


@video_router.post("/watch/{video_id}/set_like", description="Set or delete like from video", status_code=201)
async def set_like_json(video_id: int):
    return await set_like(video_id)


@video_router.delete("/watch/{video_id}/delete_video", description="Delete video")
async def delete_video(video_id: int):
    video = await http404_error_handler(class_model=Video, attribute=video_id, video=True)
    return {"status": "Successful!", "deleted_rows": await video.delete()}
