from pydantic import BaseModel

class ContainerInfo(BaseModel):
    video_uuid: str
    task_arn: str
    cluster_name: str
    file_key: str