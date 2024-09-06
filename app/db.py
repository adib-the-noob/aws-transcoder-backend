from pymongo import MongoClient

db_dependency = MongoClient(
    "mongodb://root:root@localhost:27017"
)

db_dependency = db_dependency['transcoder_app_db']

# channel index
db_dependency.channels.create_index("owner_id")

db_dependency.videos.create_index('title')
db_dependency.videos.create_index('description')
db_dependency.videos.create_index('channel_id')
db_dependency.videos.create_index('owner_id')
db_dependency.videos.create_index('visibility')
db_dependency.videos.create_index('video_uuid')
