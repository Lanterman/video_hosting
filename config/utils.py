import ormar

from fastapi import HTTPException, status

from .db import metadata, database


class MainMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


async def http404_error_handler(class_model, attribute, video=False):
    try:
        if video:
            obj = await class_model.objects.get(id=attribute)
        else:
            obj = await class_model.objects.select_related("video_set").get(username=attribute)
    except ormar.NoMatch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")
    return obj
