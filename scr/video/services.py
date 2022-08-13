import aiofiles
import os

from uuid import uuid4

from fastapi import UploadFile, HTTPException, status, BackgroundTasks

from config.utils import http404_error_handler, BASE_DIR
from scr.user.models import Users
from .models import Video


CONTENT_TYPES = ["video/mp4", "video/ogg", "video/webm"]


async def save_video(back_task: BackgroundTasks, name: str, description: str, file: UploadFile, user: Users) -> Video:
    """Save video to database and user directory"""

    file_name = f'uploaded_files/{user.id}/{uuid4()}.mp4'
    if file.content_type in CONTENT_TYPES:
        back_task.add_task(write_video, file_name, file)
    else:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported content type! Must be mp4, webm or ogg!"
        )
    return await Video.objects.create(name=name, description=description, path_to_file=file_name, user=user)


async def write_video(file_name: str, file: UploadFile) -> None:
    """Upload video to user directory"""

    async with aiofiles.open(file_name, "wb") as buffer:
        data = await file.read()
        await buffer.write(data)


async def set_like(video_id: int, user: Users) -> int:
    """Set or delete user like from video"""

    video = await http404_error_handler(class_model=Video, attribute=video_id, set_like=True)
    if user in video.like_users:
        await video.like_users.remove(user)
    else:
        await video.like_users.add(user)
    return await video.like_users.count()


def delete_video_from_user_directory(path: str, user_id: int) -> None:
    """Delete video from user directory"""

    path_to_list = path.split("/")
    if path_to_list[-1] in os.listdir(path=f"{BASE_DIR}/uploaded_files/{user_id}"):
        os.remove(path)


async def get_all_video() -> Video:
    """Get all video"""
    list_video = await Video.objects.select_related("user").all()
    return list_video


async def delete_video_from_database(video: Video, back_task: BackgroundTasks, user_id: int) -> None:
    """Delete video form database and user directory"""

    await video.delete()
    back_task.add_task(delete_video_from_user_directory, video.path_to_file, user_id)
