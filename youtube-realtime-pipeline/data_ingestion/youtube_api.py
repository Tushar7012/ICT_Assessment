from googleapiclient.discovery import build
from datetime import datetime
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

if not YOUTUBE_API_KEY:
    raise ValueError("YOUTUBE_API_KEY not found in .env file!")

youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

def fetch_video_metadata_sync(video_id: str) -> dict:
    """Fetch complete metadata for a single video (synchronous)"""
    try:
        request = youtube.videos().list(
            part="snippet,statistics,contentDetails",
            id=video_id
        )
        response = request.execute()
        
        if not response.get('items'):
            logger.warning(f"No metadata found for video: {video_id}")
            return None
        
        item = response['items'][0]
        snippet = item['snippet']
        statistics = item.get('statistics', {})
        
        metadata = {
            "video_id": video_id,
            "title": snippet['title'],
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "upload_date": snippet['publishedAt'],
            "view_count": int(statistics.get('viewCount', 0)),
            "like_count": int(statistics.get('likeCount', 0)),
            "description": snippet.get('description', '')[:500],  # Limit description length
            "channel_id": snippet['channelId'],
            "channel_title": snippet['channelTitle'],
            "tags": snippet.get('tags', [])[:10],  # Limit tags
            "duration": item['contentDetails'].get('duration', ''),
            "ingested_at": datetime.utcnow().isoformat()
        }
        
        return metadata
        
    except Exception as e:
        logger.error(f"Error fetching video {video_id}: {str(e)}")
        return None

async def fetch_video_metadata(video_id: str) -> dict:
    """Async wrapper for fetch_video_metadata_sync"""
    return fetch_video_metadata_sync(video_id)

async def fetch_channel_videos(channel_id: str, max_results: int = 5000) -> list:
    """Fetch most recent videos from a channel"""
    videos = []
    next_page_token = None
    
    try:
        logger.info(f"Starting to fetch videos for channel: {channel_id}")
        
        while len(videos) < max_results:
            logger.info(f"Fetching videos... Current count: {len(videos)}/{max_results}")
            
            request = youtube.search().list(
                part="id,snippet",
                channelId=channel_id,
                maxResults=min(50, max_results - len(videos)),
                order="date",
                type="video",
                pageToken=next_page_token
            )
            
            response = request.execute()
            
            if not response.get('items'):
                logger.warning(f"No items returned from YouTube API for channel {channel_id}")
                break
            
            # Extract video IDs
            video_ids = [item['id']['videoId'] for item in response['items'] if item['id']['kind'] == 'youtube#video']
            
            logger.info(f"Fetched {len(video_ids)} video IDs from this page")
            
            # Fetch detailed metadata for each video
            for video_id in video_ids:
                metadata = fetch_video_metadata_sync(video_id)
                if metadata:
                    videos.append(metadata)
                    
                if len(videos) % 100 == 0:
                    logger.info(f"✓ Progress: {len(videos)}/{max_results} videos processed")
            
            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                logger.info("No more pages available")
                break
        
        logger.info(f"Successfully fetched {len(videos)} videos from channel {channel_id}")
        return videos[:max_results]
        
    except Exception as e:
        logger.error(f"Error fetching channel videos: {str(e)}")
        logger.exception(e)  # Print full traceback
        return videos
