from fastapi import APIRouter, Form, File, UploadFile, Depends, BackgroundTasks, HTTPException, status
from fastapi.responses import StreamingResponse

from config.utils import http404_error_handler
from config.dependecies import get_current_user
from scr.user.models import Users
from .models import Video
from .schemas import CreateVideo, GetVideoList
from scr.video import services


video_router = APIRouter(prefix="/video", tags=["video"])


@video_router.get("/", response_model=list[GetVideoList], description="Video list output")
async def get_video_list():
    """Get all video"""

    list_video = await services.get_all_video()
    return list_video


@video_router.post("/create_video", response_model=CreateVideo, status_code=201, description="Download video file")
async def create_video(
        back_task: BackgroundTasks, name: str = Form(), description: str = Form(), file: UploadFile = File(),
        current_user: Users = Depends(get_current_user)
):
    """Create video"""

    return await services.save_video(back_task, name=name, description=description, file=file, user=current_user)


@video_router.get("/watch/{video_id}", description="Watch streaming video")
async def get_video(video_id: int):
    """Streaming video"""

    video = await http404_error_handler(class_model=Video, attribute=video_id)
    open_video = open(video.path_to_file, "rb")
    media_type = f"video/{video.path_to_file[-3:]}"
    return StreamingResponse(open_video, media_type=media_type)


@video_router.get("/watch/{video_id}/set_like", description="Set or delete like from video", status_code=201)
async def set_like(video_id: int, current_user: Users = Depends(get_current_user)):
    """Set or delete like"""

    return await services.set_like(video_id, current_user)


@video_router.delete("/watch/{video_id}/delete_video", description="Delete video")
async def delete_video(back_task: BackgroundTasks, video_id: int, current_user: Users = Depends(get_current_user)):
    """Delete video"""

    video = await http404_error_handler(class_model=Video, attribute=video_id)

    if current_user != video.user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can't do it!")

    await services.delete_video_from_database(video=video, back_task=back_task, user_id=current_user.id)
    return {"status": "Successful!"}
