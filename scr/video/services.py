import aiofiles
from uuid import uuid4

from fastapi import UploadFile, HTTPException, status

from config.utils import http404_error_handler
from scr.user.models import Users
from .models import Video


CONTENT_TYPES = ["video/mp4", "video/ogg", "video/webm"]


async def save_video(name: str, description: str, file: UploadFile, user: Users):
    file_name = f'uploaded_files/{user.id}/{uuid4()}.mp4'
    if file.content_type in CONTENT_TYPES:
        await write_video(file_name=file_name, file=file)
    else:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported content type! Must be mp4, webm or ogg!"
        )
    return await Video.objects.create(name=name, description=description, path_to_file=file_name, user=user)


async def write_video(file_name: str, file: UploadFile):
    async with aiofiles.open(file_name, "wb") as buffer:
        data = await file.read()
        await buffer.write(data)


async def set_like(video_id: int):
    video = await http404_error_handler(class_model=Video, attribute=video_id, set_like=True)
    user = await Users.objects.first()
    if user in video.like_users:
        await video.like_users.remove(user)
    else:
        await video.like_users.add(user)
    return await video.like_users.count()
