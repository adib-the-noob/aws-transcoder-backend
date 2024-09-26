from fastapi import APIRouter, Depends, Query, status, HTTPException

from db import db_dependency
from models.video_models import (
    Video
)

router = APIRouter(
    prefix="/video",
    tags=["video"]
)


@router.get("/video-search")
async def search_video(
    db: db_dependency,
    query: str = Query(None, description="Search query for title and description")
):
    pass

