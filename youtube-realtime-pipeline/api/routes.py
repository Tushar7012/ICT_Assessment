from fastapi import APIRouter, Query, HTTPException, Depends
from database.query_operations import (
    get_recent_videos,
    count_videos_by_channel,
    search_videos_by_keyword,
    get_channel_statistics,
    count_videos_in_timerange
)
from api.auth import verify_api_key

router = APIRouter(prefix="/api", tags=["videos"])

@router.get("/videos/recent")
async def get_recent(
    limit: int = Query(10, ge=1, le=100),
    api_key: str = Depends(verify_api_key)
):
    """Get most recent videos"""
    videos = get_recent_videos(limit)
    return {"status": "success", "count": len(videos), "videos": videos}

@router.get("/videos/search")
async def search_videos(
    keyword: str = Query(..., min_length=1),
    limit: int = Query(10, ge=1, le=50),
    api_key: str = Depends(verify_api_key)
):
    """Search videos by keyword"""
    videos = search_videos_by_keyword(keyword, limit)
    return {"status": "success", "count": len(videos), "keyword": keyword, "videos": videos}

@router.get("/videos/trending")
async def get_trending_videos(
    limit: int = Query(10, ge=1, le=50),
    api_key: str = Depends(verify_api_key)
):
    """Get trending videos sorted by views"""
    from database.mongodb_client import get_sync_database
    db = get_sync_database()
    
    cursor = db['videos'].find().sort("view_count", -1).limit(limit)
    videos = list(cursor)
    
    for video in videos:
        video['_id'] = str(video['_id'])
    
    return {"status": "success", "count": len(videos), "videos": videos}

@router.get("/videos/count/{channel_name}")
async def count_channel_videos(
    channel_name: str,
    api_key: str = Depends(verify_api_key)
):
    """Count total videos from a channel"""
    count = count_videos_by_channel(channel_name)
    return {"status": "success", "channel": channel_name, "video_count": count}

@router.get("/videos/channel/{channel_name}/stats")
async def get_channel_stats(
    channel_name: str,
    api_key: str = Depends(verify_api_key)
):
    """Get detailed channel statistics"""
    stats = get_channel_statistics(channel_name)
    if not stats:
        raise HTTPException(status_code=404, detail=f"Channel '{channel_name}' not found")
    return {"status": "success", "channel": channel_name, "statistics": stats}

@router.get("/videos/channel/{channel_name}/recent")
async def get_channel_recent_videos(
    channel_name: str,
    hours: int = Query(24, ge=1, le=720),
    api_key: str = Depends(verify_api_key)
):
    """Get recent videos from channel in timeframe"""
    count = count_videos_in_timerange(channel_name, hours)
    return {"status": "success", "channel": channel_name, "hours": hours, "video_count": count}
