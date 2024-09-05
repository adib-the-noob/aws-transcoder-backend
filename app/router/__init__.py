from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

@router.get("/create-user")
async def create_user():
    return JSONResponse({
        "message": "User created successfully"
    })