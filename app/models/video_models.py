# from sqlalchemy import Column, Integer, String
# from db import Base
# from .baseModelMixin import BaseModelMixin

# class Video(BaseModelMixin, Base):
#     __tablename__ = "videos"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String)
#     description = Column(String)
#     file_path = Column(String)
#     channel_id = Column(Integer)

#     def __repr__(self):
#         return f"<Video - {self.title}>"
    
#     def __str__(self):
#         return f"<Video - {self.title}>"
    
#     def __init__(self, title, description, file_path, channel_id):
#         self.title = title
#         self.description = description
#         self.file_path = file_path
#         self.channel_id = channel_id