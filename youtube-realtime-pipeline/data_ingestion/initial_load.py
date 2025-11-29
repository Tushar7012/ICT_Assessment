import asyncio
from data_ingestion.youtube_api import fetch_channel_videos
from database.mongodb_client import get_sync_database
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Target channels
CHANNELS = {
    "UCnKJeK_r90jDdIuzHXC0Org": "markets (Bloomberg Television)",
    "UCFx1nseXKTc1Culiu3neeSQ": "ANI News India",
}

async def load_initial_data():
    """Load initial 5000 videos from each target channel"""
    logger.info("="*60)
    logger.info("Starting Initial Data Load")
    logger.info("="*60)
    
    db = get_sync_database()
    collection = db['videos']
    
    total_loaded = 0
    
    for channel_id, channel_name in CHANNELS.items():
        logger.info(f"\n📺 Processing: {channel_name}")
        logger.info(f"Channel ID: {channel_id}")
        
        start_time = datetime.now()
        videos = await fetch_channel_videos(channel_id, max_results=5000)
        
        if not videos:
            logger.warning(f"No videos fetched from {channel_name}")
            continue
        
        logger.info(f"Storing {len(videos)} videos in MongoDB...")
        
        new_count = 0
        for i, video in enumerate(videos, 1):
            try:
                result = collection.update_one(
                    {"video_id": video["video_id"]},
                    {"$set": video},
                    upsert=True
                )
                
                if result.upserted_id:
                    new_count += 1
                
                if i % 500 == 0:
                    logger.info(f"  Progress: {i}/{len(videos)} videos processed")
                    
            except Exception as e:
                logger.error(f"Error storing video {video['video_id']}: {str(e)}")
        
        elapsed_time = (datetime.now() - start_time).total_seconds()
        
        logger.info(f"\n✓ {channel_name} Summary:")
        logger.info(f"  New videos: {new_count}")
        logger.info(f"  Time taken: {elapsed_time:.2f} seconds")
        
        total_loaded += new_count
    
    logger.info("\n" + "="*60)
    logger.info("Initial Data Load Complete!")
    logger.info(f"Total new videos: {total_loaded}")
    logger.info(f"Total videos in database: {collection.count_documents({})}")
    logger.info("="*60)

if __name__ == "__main__":
    asyncio.run(load_initial_data())
