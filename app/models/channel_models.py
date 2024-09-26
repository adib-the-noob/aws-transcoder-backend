from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Relationship
from sqlalchemy.sql.schema import ForeignKey

from db import Base
from .baseModelMixin import BaseModelMixin

class Channel(Base, BaseModelMixin):
    __tablename__ = "channels"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = Relationship("User", back_populates="channels")
    
    # Define the relationship to Video as plural
    videos = Relationship("Video", back_populates="channel")
    
    def __repr__(self) -> str:
        return f"<Channel - {self.name}>"
    
    def __str__(self) -> str:
        return f"<Channel - {self.name}>"