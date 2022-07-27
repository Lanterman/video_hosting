import aiofiles
from uuid import uuid4

from fastapi import UploadFile, HTTPException, status

from user.models import User
from .models import Video


CONTENT_TYPES = ["video/mp4", "video/ogg", "video/webm"]


async def save_video(name: str, description: str, file: UploadFile, user: User):
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
