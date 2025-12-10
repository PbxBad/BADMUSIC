from motor.motor_asyncio import AsyncIOMotorClient as _mongo_client_
from pymongo import MongoClient
from pyrogram import Client

import config

from ..logging import LOGGER

TEMP_MONGODB = "mongodb+srv://BADMUNDA:BADMYDAD@badhacker.i5nw9na.mongodb.net/"

# --- MODIFIED: Define variables but set them to None initially ---
_mongo_async_ = None
_mongo_sync_ = None
mongodb = None
pymongodb = None
# -----------------------------------------------------------------

async def init():
    """Initializes both the synchronous (pymongo) and asynchronous (motor) clients."""
    global _mongo_async_, _mongo_sync_, mongodb, pymongodb

    if config.MONGO_DB_URI is None:
        LOGGER(__name__).warning(
            "𝐍o 𝐌ONGO 𝐃B 𝐔RL 𝐅ound.. 𝐘our 𝐁ot 𝐖ill 𝐖ork 𝐎n 𝐁ᴀᴅ 𝐌𝐔𝐒𝐈𝐂 𝐃atabase"
        )
        # Note: We use an async context here, so Pyrogram is safe to run.
        async with Client(
            "BADMUSIC",
            bot_token=config.BOT_TOKEN,
            api_id=config.API_ID,
            api_hash=config.API_HASH,
        ) as temp_client:
            info = await temp_client.get_me()
            username = info.username
            
            # --- MODIFIED: Initialization now happens inside the async function ---
            _mongo_async_ = _mongo_client_(TEMP_MONGODB)
            _mongo_sync_ = MongoClient(TEMP_MONGODB)
            mongodb = _mongo_async_[username]
            pymongodb = _mongo_sync_[username]
            # ---------------------------------------------------------------------

    else:
        # --- MODIFIED: Initialization now happens inside the async function ---
        _mongo_async_ = _mongo_client_(config.MONGO_DB_URI)
        _mongo_sync_ = MongoClient(config.MONGO_DB_URI)
        mongodb = _mongo_async_.BADMUSIC
        pymongodb = _mongo_sync_.BADMUSIC
        # ---------------------------------------------------------------------

