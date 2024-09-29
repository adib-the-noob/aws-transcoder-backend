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
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"
    UNLISTED = "UNLISTED"
    
class Video(Base, BaseModelMixin):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    video_uuid = Column(String, index=True)
    s3_key = Column(String)
    bucket_name = Column(String)
    
    thumbnail = Column(String)
    transcoding_status = Column(Enum(TranscodingStatus), default=TranscodingStatus.PENDING)
    visibility = Column(Enum(VideoVisibility), default=VideoVisibility.PUBLIC)
    
    channel_id = Column(Integer, ForeignKey("channels.id"))
    channel = Relationship("Channel", back_populates="videos")
    
    quality = Relationship("Quality", back_populates="video")
    
    def __repr__(self):
        return f"<Video - {self.title}>"
    
    def __str__(self):
        return f"<Video - {self.title}>"
    
    
class Quality(Base, BaseModelMixin):
    __tablename__ = 'qualities'
    
    id = Column(Integer, primary_key=True, index=True)
    dimension = Column(String)
    url = Column(String)
    
    video_id = Column(Integer, ForeignKey("videos.id"))
    video = Relationship("Video", back_populates="quality")
    
    def __repr__(self):
        return f"<Quality - {self.dimension}>"
    
    def __str__(self):
        return f"<Quality - {self.dimension}>"