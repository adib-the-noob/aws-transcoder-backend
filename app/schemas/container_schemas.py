from pydantic import BaseModel

class ContainerInfo(BaseModel):
    video_uuid: str
    ecs_task_info: dict