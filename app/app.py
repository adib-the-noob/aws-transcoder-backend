from fastapi import FastAPI

from router import (
    user_authentication
)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(user_authentication.router)
