from fastapi import APIRouter, HTTPException, Depends, status, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.params import Query

from db import db_dependency
from schemas.container_schemas import ContainerInfo
from aws.ecs_task_utils import (
    get_task_public_ip,
    update_task_public_ip
)

from bson import ObjectId

router = APIRouter(
    prefix="/container_infos",
    tags=["container_infos"]
)

@router.post("/add-task-info")
async def add_task_info(
    create_task_info: ContainerInfo,
    background_tasks: BackgroundTasks
):
    try:
        inserted_task_info = db_dependency.container_infos.insert_one({
            "video_uuid": create_task_info.video_uuid,
            "file_key": create_task_info.file_key,
            "task_arn": create_task_info.task_arn,
            "cluster_name": create_task_info.cluster_name,
        })
        
        background_tasks.add_task(
            update_task_public_ip,
            inserted_task_info.inserted_id,
            create_task_info.task_arn,
            create_task_info.cluster_name
         )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "id": str(inserted_task_info.inserted_id),
                "video_uuid": create_task_info.video_uuid,
            }
        )
        
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(e)}
        )
        
        
@router.get("/get-task-info")
async def get_task_info(
    uuid: str = Query(..., alias="video_uuid")
):
    try:
        task_info = db_dependency.container_infos.find_one({
            "video_uuid": uuid
        })
        if task_info is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task info not found"
            )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "id": str(task_info["_id"]),
                "video_uuid": task_info["video_uuid"],
                "file_key": task_info["file_key"],
                "task_arn": task_info["task_arn"],
                "cluster_name": task_info["cluster_name"],
                "public_ip": task_info["public_ip"]
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(e)}
        )
        