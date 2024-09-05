from fastapi import FastAPI

from router import (
    user_authentication,
    channels_create
)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(user_authentication.router)
app.include_router(channels_create.router)