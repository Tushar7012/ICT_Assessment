from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
import os
from pathlib import Path
from dotenv import load_dotenv
import logging

# Load .env from project root
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MONGODB_URL = os.getenv("MONGODB_URL")

if not MONGODB_URL:
    logger.error("MONGODB_URL not found in environment variables!")
    raise ValueError("MONGODB_URL environment variable is not set. Check your .env file.")

logger.info(f"MongoDB URL loaded: {MONGODB_URL[:30]}...")  # Show first 30 chars for debugging

# Async client for FastAPI
async_client = None
async_db = None

def get_database():
    """Get async MongoDB database for FastAPI"""
    global async_client, async_db
    if async_db is None:
        async_client = AsyncIOMotorClient(MONGODB_URL)
        async_db = async_client['youtube_pipeline']
        logger.info("Connected to MongoDB (async)")
    return async_db

# Sync client for scripts
sync_client = None
sync_db = None

def get_sync_database():
    """Get synchronous MongoDB database for scripts"""
    global sync_client, sync_db
    if sync_db is None:
        sync_client = MongoClient(MONGODB_URL)
        sync_db = sync_client['youtube_pipeline']
        logger.info("Connected to MongoDB Atlas (sync)")
    return sync_db

def close_connections():
    """Close all database connections"""
    global async_client, sync_client
    if async_client:
        async_client.close()
    if sync_client:
        sync_client.close()
    logger.info("Database connections closed")
