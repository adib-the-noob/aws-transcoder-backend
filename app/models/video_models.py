from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Relationship
from sqlalchemy.sql.schema import ForeignKey
   
from db import Base
from .baseModelMixin import BaseModelMixin

class Video(BaseModelMixin, Base):
    __tablename__ = "videos"

    title = Column(String, index=True)
    description = Column(String)
    s3_key = Column(String)
    
    channel_id = Column(Integer, ForeignKey("channels.id"))
    channel = Relationship("Channel", back_populates="videos")
    
    def __repr__(self):
        return f"<Video - {self.title}>"
    
    def __str__(self):
        return f"<Video - {self.title}>"
    