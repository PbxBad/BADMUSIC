from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import config

mongo_async = None
mongo_sync = None
mongodb = None
pymongodb = None


def init_mongo(db_name="BADMUSIC"):
    global mongo_async, mongo_sync, mongodb, pymongodb

    uri = config.MONGO_DB_URI
    if not uri:
        raise RuntimeError("Mongo DB URI not found!")

    mongo_async = AsyncIOMotorClient(uri)
    mongo_sync = MongoClient(uri)

    mongodb = mongo_async[db_name]
    pymongodb = mongo_sync[db_name]
