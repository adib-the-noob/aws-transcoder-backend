from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Relationship
from sqlalchemy.sql.schema import ForeignKey

from db import Base
from .baseModelMixin import BaseModelMixin

class User(Base, BaseModelMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

    channels = Relationship("Channel", back_populates="owner")


    def __repr__(self):
        return f"<User - {self.email}>"
    
    def __str__(self):
        return f"<User - {self.email}>"
    