from pymongo import MongoClient

db_dependency = MongoClient(
    "mongodb://root:root@localhost:27017"
)

db_dependency = db_dependency['transcoder_app_db']