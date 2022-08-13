import ormar

from pathlib import Path

from fastapi import HTTPException, status

from .db import metadata, database


BASE_DIR = Path(__file__).resolve().parent.parent


class MainMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


async def http404_error_handler(class_model, attribute, set_like=False):
    try:
        if not set_like:
            obj = await class_model.objects.get(id=attribute)
        else:
            obj = await class_model.objects.select_related("like_users").get(id=attribute)
    except ormar.NoMatch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")
    return obj
