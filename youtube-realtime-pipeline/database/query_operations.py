from database.mongodb_client import get_sync_database
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_recent_videos(limit: int = 10) -> list:
    """Get most recent videos from database"""
    db = get_sync_database()
    cursor = db['videos'].find().sort("upload_date", -1).limit(limit)
    videos = list(cursor)
    
    # Convert ObjectId to string
    for video in videos:
        video['_id'] = str(video['_id'])
    
    return videos

def search_videos_by_keyword(keyword: str, limit: int = 10) -> list:
    """Search videos by keyword in title or description"""
    db = get_sync_database()
    
    # Case-insensitive search in title and description
    query = {
        "$or": [
            {"title": {"$regex": keyword, "$options": "i"}},
            {"description": {"$regex": keyword, "$options": "i"}},
            {"tags": {"$regex": keyword, "$options": "i"}}
        ]
    }
    
    cursor = db['videos'].find(query).sort("upload_date", -1).limit(limit)
    videos = list(cursor)
    
    for video in videos:
        video['_id'] = str(video['_id'])
    
    logger.info(f"Found {len(videos)} videos matching keyword: {keyword}")
    return videos

def count_videos_by_channel(channel_name: str) -> int:
    """Count videos by channel name (partial match)"""
    db = get_sync_database()
    
    # Case-insensitive partial match on channel_title
    query = {"channel_title": {"$regex": channel_name, "$options": "i"}}
    count = db['videos'].count_documents(query)
    
    logger.info(f"Found {count} videos for channel: {channel_name}")
    return count

def get_channel_statistics(channel_name: str) -> dict:
    """Get aggregate statistics for a channel"""
    db = get_sync_database()
    
    pipeline = [
        {
            "$match": {
                "channel_title": {"$regex": channel_name, "$options": "i"}
            }
        },
        {
            "$group": {
                "_id": "$channel_title",
                "total_videos": {"$sum": 1},
                "total_views": {"$sum": "$view_count"},
                "total_likes": {"$sum": "$like_count"},
                "avg_views": {"$avg": "$view_count"},
                "avg_likes": {"$avg": "$like_count"}
            }
        }
    ]
    
    result = list(db['videos'].aggregate(pipeline))
    
    if not result:
        return None
    
    stats = result[0]
    stats.pop('_id', None)  # Remove _id field
    
    logger.info(f"Statistics for {channel_name}: {stats}")
    return stats

def count_videos_in_timerange(channel_name: str, hours: int) -> int:
    """Count videos uploaded in last X hours for a channel"""
    db = get_sync_database()
    
    time_threshold = (datetime.utcnow() - timedelta(hours=hours)).isoformat()
    
    query = {
        "channel_title": {"$regex": channel_name, "$options": "i"},
        "upload_date": {"$gte": time_threshold}
    }
    
    count = db['videos'].count_documents(query)
    logger.info(f"Found {count} videos in last {hours} hours for {channel_name}")
    return count
