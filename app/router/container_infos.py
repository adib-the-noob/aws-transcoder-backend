from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse

from db import db_dependency
from schemas.container_schemas import ContainerInfo
from aws.ecs_task_utils import get_public_ip_of_task

router = APIRouter(
    prefix="/container_infos",
    tags=["container_infos"]
)

@router.post("/add-task-info")
async def add_task_info(
    task_info: ContainerInfo,
):
    try:
        public_ip = get_public_ip_of_task(task_info.ecs_task_info)
        inserted_task_info = db_dependency.container_infos.insert_one({
            "video_uuid": task_info.video_uuid,
            "public_ip": public_ip,
            "ecs_task_info": task_info.ecs_task_info,
        })
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "video_uuid": task_info.video_uuid,
                "task_id": str(inserted_task_info.inserted_id),
                "task_info": task_info.ecs_task_info
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(e)}
        )