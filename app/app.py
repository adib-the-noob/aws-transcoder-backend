from fastapi import FastAPI

from router import (
    user_authentication,
    channels_create,
    video_uploader,
    video_info,
    container_infos
)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(user_authentication.router)
app.include_router(channels_create.router)
app.include_router(video_uploader.router)
app.include_router(video_info.router)
app.include_router(container_infos.router)
