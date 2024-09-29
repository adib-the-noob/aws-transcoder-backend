from fastapi import APIRouter, Depends, Query, status, HTTPException

from db import db_dependency
from models.video_models import (
    Video
)
from models.video_models import (
    Quality
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
    video_data = db.query(Video).filter(Video.title.ilike(f"%{query}%")).all()
    # quality_data = db.query(Quality).filter(Quality.video_id == Video.id).all()
    
    video_datas = []
    for video in video_data:
        video_datas.append({
            "video": video,
            # "qualities": [quality for quality in quality_data if quality.video_id == video.id]
        })
    
    return video_datas

@router.get("/video-data/{video_id}")
async def search_video(
    id: int,
    db: db_dependency,
):
    video_data = db.query(Video).filter(Video.id==id).all()
    quality_data = db.query(Quality).filter(Quality.video_id == Video.id).all()
    
    video_datas = []
    for video in video_data:
        video_datas.append({
            "video": video,
            "qualities": [quality for quality in quality_data if quality.video_id == video.id]
        })
    
    return video_datas

        
        
        
        