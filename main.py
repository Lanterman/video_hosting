from fastapi import FastAPI

from config.db import metadata, database, engine
from scr.user.api import user_router
from scr.video.api import video_router
from scr.video.html_api import html_router

app = FastAPI()

metadata.create_all(engine)
app.state.database = database


@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()


app.include_router(video_router)
app.include_router(user_router)
app.include_router(html_router)


print("вывод сразу всех ошибок валидации")
