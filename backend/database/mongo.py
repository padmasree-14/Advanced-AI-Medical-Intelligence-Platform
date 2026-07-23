import logging
import asyncio
from typing import Optional, Dict, Any
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from backend.config.settings import settings

logger = logging.getLogger(__name__)

class MongoDBManager:
    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None
    is_connected: bool = False

    @classmethod
    async def connect(cls):
        try:
            logger.info(f"Connecting to MongoDB at {settings.MONGODB_URL}...")
            cls.client = AsyncIOMotorClient(
                settings.MONGODB_URL,
                serverSelectionTimeoutMS=2000
            )
            # Ping to confirm connection
            await cls.client.admin.command('ping')
            cls.db = cls.client[settings.MONGODB_DB_NAME]
            cls.is_connected = True
            logger.info(f"Successfully connected to MongoDB database: '{settings.MONGODB_DB_NAME}'")
            await cls.init_indexes()
        except Exception as e:
            logger.warning(f"MongoDB connection failed: {e}. Falling back to resilient in-memory repository store.")
            cls.is_connected = False

    @classmethod
    async def close(cls):
        if cls.client:
            cls.client.close()
            logger.info("MongoDB connection closed.")

    @classmethod
    async def init_indexes(cls):
        if cls.db is not None:
            try:
                await cls.db.users.create_index("email", unique=True)
                await cls.db.users.create_index("username", unique=True)
                await cls.db.predictions.create_index("user_id")
                await cls.db.reports.create_index("prediction_id")
                await cls.db.audit_logs.create_index("timestamp")
                logger.info("MongoDB indexes verified successfully.")
            except Exception as e:
                logger.error(f"Error creating indexes: {e}")

db_manager = MongoDBManager()
