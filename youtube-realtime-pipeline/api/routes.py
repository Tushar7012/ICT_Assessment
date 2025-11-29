from fastapi import APIRouter, Depends, Query, HTTPException
from database.query_operations import (
    get_recent_videos,
    count_videos_by_channel,
    search_videos_by_keyword,
    get_channel_statistics
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
    return {"count": len(videos), "videos": videos}

@router.get("/videos/search")
async def search_videos(
    keyword: str = Query(..., min_length=1),
    limit: int = Query(10, ge=1, le=50),
    api_key: str = Depends(verify_api_key)
):
    """Search videos by keyword"""
    videos = search_videos_by_keyword(keyword, limit)
    return {"count": len(videos), "keyword": keyword, "videos": videos}

@router.get("/videos/count/{channel_name}")
async def count_channel(
    channel_name: str,
    api_key: str = Depends(verify_api_key)
):
    """Count videos by channel"""
    count = count_videos_by_channel(channel_name)
    return {"channel": channel_name, "video_count": count}

@router.get("/stats/{channel_name}")
async def channel_stats(
    channel_name: str,
    api_key: str = Depends(verify_api_key)
):
    """Get channel statistics"""
    stats = get_channel_statistics(channel_name)
    if not stats:
        raise HTTPException(status_code=404, detail="Channel not found")
    return {"channel": channel_name, "statistics": stats}
