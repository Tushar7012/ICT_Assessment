#!/usr/bin/env python3
"""
Query script for database testing (Deliverable #1)
Usage: python scripts/query_db.py --limit 10
"""

from database.mongodb_client import get_sync_database
from database.query_operations import (
    get_recent_videos,
    count_videos_by_channel,
    count_videos_in_timerange
)
import argparse
import json

def main():
    parser = argparse.ArgumentParser(description="Query YouTube video database")
    parser.add_argument("--limit", type=int, default=10, help="Number of videos to retrieve")
    parser.add_argument("--channel", type=str, help="Channel name to query")
    parser.add_argument("--hours", type=int, help="Time range in hours")
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("YouTube Video Database Query")
    print("="*60 + "\n")
    
    # Test 1: Get recent videos
    print(f"📺 Most Recent {args.limit} Videos:")
    print("-" * 60)
    videos = get_recent_videos(args.limit)
    
    for i, video in enumerate(videos, 1):
        print(f"\n{i}. {video['title']}")
        print(f"   Channel: {video['channel_title']}")
        print(f"   Views: {video['view_count']:,} | Likes: {video['like_count']:,}")
        print(f"   Uploaded: {video['upload_date']}")
        print(f"   URL: {video['url']}")
    
    # Test 2: Count by channel (for Prompt 1)
    print("\n" + "="*60)
    print("📊 Channel Statistics")
    print("="*60)
    
    channels = ["markets", "Bloomberg", "ANI", "ANINews"]
    for channel in channels:
        count = count_videos_by_channel(channel)
        if count > 0:
            print(f"   {channel}: {count} videos")
    
    # Test 3: Time-based count (for Prompt 2)
    if args.channel and args.hours:
        print("\n" + "="*60)
        print(f"⏰ Videos in Last {args.hours} Hours")
        print("="*60)
        count = count_videos_in_timerange(args.channel, args.hours)
        print(f"   {args.channel}: {count} videos in last {args.hours} hours")
    
    # Database summary
    db = get_sync_database()
    total = db['videos'].count_documents({})
    print("\n" + "="*60)
    print(f"Total videos in database: {total}")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
