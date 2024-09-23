import datetime

from sqlalchemy import Column, Integer, String
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Session

from db import Base


class BaseModelMixin:
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)

    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now) 
    
    def save(self, db : Session):
        db.add(self)
        db.commit()
        db.refresh(self)
        return self
    
    def delete(self, db : Session):
        db.delete(self)
        db.commit()
        return self
    
    
    