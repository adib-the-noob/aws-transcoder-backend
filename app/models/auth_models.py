from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Relationship


from db import Base
from .baseModelMixin import BaseModelMixin

class User(BaseModelMixin, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    def __repr__(self):
        return f"<User - {self.email}>"
    
    def __str__(self):
        return f"<User - {self.email}>"
    