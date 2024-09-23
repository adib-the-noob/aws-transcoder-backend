from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import Relationship
from sqlalchemy.sql.schema import ForeignKey
   
from enum import Enum as PyEnum 
from db import Base
from .baseModelMixin import BaseModelMixin


class TranscodingStatus(PyEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    PUBLISHED = "published"

class VideoVisibility(PyEnum):
    PUBLIC = "public"
    PRIVATE = "private"
    UNLISTED = "unlisted"
    
class Video(BaseModelMixin, Base):
    __tablename__ = "videos"

    title = Column(String, index=True)
    description = Column(String)
    s3_key = Column(String)
    
    transcoding_status = Column(Enum(TranscodingStatus), default=TranscodingStatus.PENDING)
    visibility = Column(Enum(VideoVisibility), default=VideoVisibility.PUBLIC)
    
    channel_id = Column(Integer, ForeignKey("channels.id"))
    channel = Relationship("Channel", back_populates="videos")
    
    def __repr__(self):
        return f"<Video - {self.title}>"
    
    def __str__(self):
        return f"<Video - {self.title}>"
    