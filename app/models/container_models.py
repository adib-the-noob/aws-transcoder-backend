from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Relationship
from sqlalchemy.sql.schema import ForeignKey

from db import Base
from .baseModelMixin import BaseModelMixin

class Container(Base, BaseModelMixin):
    __tablename__ = "containers"
    
    id = Column(Integer, primary_key=True, index=True) 
    arn = Column(String, index=True)
    tag = Column(String)
    public_ip = Column(String)
    port = Column(Integer)
    description = Column(String)
    
    def get_container_url(self):
        return f"http://{self.public_ip}:{self.port}/"
    
    def __repr__(self) -> str:
        return f"<Container - {self.name}>"
    
    def __str__(self) -> str:
        return f"<Container - {self.name}>"
    
    