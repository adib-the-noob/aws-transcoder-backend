from pydantic import BaseModel, Field
from datetime import datetime, timezone

class CreateChannelModel(BaseModel):
    name: str = Field(...)
    description: str = Field(...)
   