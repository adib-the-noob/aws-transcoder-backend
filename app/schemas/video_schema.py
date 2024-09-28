from enum import Enum as PyEnum
from fastapi import UploadFile, File, Depends
from pydantic import BaseModel, Field


class VideoVisibility(PyEnum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"
    UNLISTED = "UNLISTED"
    

class UploadVideoModel(BaseModel):
    video_file: UploadFile = File(...)
    title: str = Field(...)
    description: str = Field(...)
    channel_id: str = Field(...)
    visibility: VideoVisibility = Field(default=VideoVisibility.PUBLIC.value)
    