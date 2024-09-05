from pydantic import BaseModel, Field
from datetime import datetime, timezone

class CreateChannelModel(BaseModel):
    name: str = Field(...)
    description: str = Field(...)
    owner_id: str = Field(None)
    created_at: str = Field(default=datetime.now(timezone.utc))
    updated_at: str = Field(default=datetime.now(timezone.utc))
    

class ChannelModel(CreateChannelModel):
    id : str = Field(...)