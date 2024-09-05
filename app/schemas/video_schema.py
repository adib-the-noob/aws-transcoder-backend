from fastapi import UploadFile, File, Depends
from pydantic import BaseModel, Field

class UploadVideoModel(BaseModel):
    video_file: UploadFile = File(...)
    title: str = Field(...)
    description: str = Field(...)
    channel_id: str = Field(...)
    visibility: str = Field(...)
    