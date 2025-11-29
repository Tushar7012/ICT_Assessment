from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from scripts.query_db import get_recent_videos, count_videos_by_channel
import os

app = FastAPI(title="YouTube Metadata API")

API_KEY = os.getenv("API_KEY", "your-secret-api-key-here")
api_key_header = APIKeyHeader(name="X-API-Key")

def verify_api_key(api_key: str = Security(api_key_header)):
    """Verify API key authentication"""
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key

@app.get("/api/videos/recent")
async def get_recent(limit: int = 10, api_key: str = Depends(verify_api_key)):
    """Get most recent videos"""
    videos = get_recent_videos(limit)
    return {"count": len(videos), "videos": videos}

@app.get("/api/videos/stats/{channel_name}")
async def get_channel_stats(channel_name: str, api_key: str = Depends(verify_api_key)):
    """Get statistics for a channel"""
    count = count_videos_by_channel(channel_name)
    return {"channel": channel_name, "video_count": count}
