from fastapi import APIRouter, HTTPException, Depends, status, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.params import Query

from db import db_dependency
from schemas.container_schemas import ContainerInfo
from aws.ecs_task_utils import (
    get_task_public_ip,
    update_task_public_ip,
    ecs
)
from models.container_models import Container
from models.video_models import Video
from models.video_models import Quality

router = APIRouter(
    prefix="/container_infos",
    tags=["container_infos"]
)

@router.post("/add-task-info")
async def add_task_info(
    create_task_info: ContainerInfo,
    background_tasks: BackgroundTasks,
    db: db_dependency
):
    try:
        video = db.query(Video).filter(Video.video_uuid == create_task_info.video_uuid).first()  
        
        if video is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Video not found"
            )
        
        container = Container(
            tag=create_task_info.video_uuid,
            arn=create_task_info.task_arn,        )
        container.save(db)
        
        background_tasks.add_task(
            update_task_public_ip,
            create_task_info.task_arn,
            create_task_info.cluster_name,
            db
         )
        
        index = db.query(Quality).filter(Quality.video_id == video.id).first()
        if index is None:
            dimensions = ["1080p", "720p", "480p", "360p"] 
            
            for dimension in dimensions:
                quality = Quality(
                    dimension=dimension,
                    url=f"https://d374zz8e4jhcib.cloudfront.net/videos/{video.video_uuid}/{dimension}/playlist.m3u8",
                    video_id=video.id
                )
                quality.save(db)    
            
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "video_uuid": create_task_info.video_uuid,
            }
        )
        
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(e)}
        )
        

        
@router.get("/transcoding-finished")
async def transcoding_finished(
    db: db_dependency,
    video_uuid: str = Query(None, description="Video UUID"),
):
    try:
        video = db.query(Video).filter(Video.video_uuid == video_uuid).first()
        
        if video is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Video not found"
            )
            
        
        video.transcoding_status = "PUBLISHED"
        video.save(db)
        
        task_info = db.query(Container).filter(Container.tag == video_uuid).first()
    
        kill_task = ecs.stop_task(
            cluster="transcoder-app-cluster",
            task=task_info.arn
        )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "video_uuid": video_uuid,
                "message": "Transcoding finished",
            }
        )
        
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(e)}
        )