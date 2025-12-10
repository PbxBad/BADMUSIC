from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import config
from ..logging import LOGGER

mongodb = None
pymongodb = None

TEMP_MONGODB = "mongodb+srv://BADMUNDA:BADMYDAD@badhacker.i5nw9na.mongodb.net/"


async def init_mongo(app):
    global mongodb, pymongodb

    try:
        # get bot username AFTER event loop starts
        me = await app.get_me()
        username = me.username or "ERAVIBES"

        if config.MONGO_DB_URI is None:
            LOGGER(__name__).warning(
                "ɴᴏ ᴍᴏɴɢᴏᴅʙ ꜰᴏᴜɴᴅ, ᴜꜱɪɴɢ ᴘᴜʙʟɪᴄ ᴍᴏɴɢᴏᴅʙ...💚"
            )

            mongo_async = AsyncIOMotorClient(TEMP_MONGODB)
            mongo_sync = MongoClient(TEMP_MONGODB)

            mongodb = mongo_async[username]
            pymongodb = mongo_sync[username]

        else:
            LOGGER(__name__).info("✦ ᴄᴏɴɴᴇᴄᴛɪɴɢ ᴛᴏ ᴄᴜꜱᴛᴏᴍ ᴍᴏɴɢᴏ...💛")

            mongo_async = AsyncIOMotorClient(config.MONGO_DB_URI)
            mongo_sync = MongoClient(config.MONGO_DB_URI)

            mongodb = mongo_async.ERAVIBES
            pymongodb = mongo_sync.ERAVIBES

        LOGGER(__name__).info("✅ MongoDB connected successfully")

    except Exception as e:
        LOGGER(__name__).error(f"❌ MongoDB connection failed: {e}")
        raise
