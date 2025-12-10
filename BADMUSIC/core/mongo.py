from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB_URI
from ..logging import LOGGER

LOGGER(__name__).info("Connecting to MongoDB...")

try:
    mongo = AsyncIOMotorClient(
        MONGO_DB_URI,
        serverSelectionTimeoutMS=5000
    )
    db = mongo.BADMUSIC
    LOGGER(__name__).info("MongoDB client initialized.")
except Exception as e:
    LOGGER(__name__).error(f"MongoDB init failed: {e}")
    raise
