import ormar

from fastapi import HTTPException, status

from .db import metadata, database


class MainMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


# def http404_error_handler(function):
#     try:
#         function()
#     except ormar.NoMatch:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")
