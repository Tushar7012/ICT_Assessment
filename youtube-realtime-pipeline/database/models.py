from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class VideoMetadata(BaseModel):
    video_id: str = Field(..., description="YouTube video ID")
    title: str
    url: str
    upload_date: str
    view_count: int
    like_count: int
    description: Optional[str] = ""
    channel_id: str
    channel_title: str
    ingested_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
