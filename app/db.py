from pymongo import MongoClient
from fastapi import Depends

db_dependency = MongoClient(
    "mongodb://root:root@localhost:27017"
)

def get_db_dependency():
    return db_dependency['transcoder_app_db']

db_dependency : Depends = get_db_dependency()

# channel index
db_dependency.channels.create_index("owner_id")

# video index
db_dependency.videos.create_index([
    ('title', 'text'),
    ('description', 'text')
])

db_dependency.videos.create_index('description')
db_dependency.videos.create_index('channel_id')
db_dependency.videos.create_index('owner_id')
db_dependency.videos.create_index('visibility')
# db_dependency.videos.drop_index('video_uuid_1')
db_dependency.videos.create_index('video_uuid', unique=True)    
