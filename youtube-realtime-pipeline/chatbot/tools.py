from database.query_operations import (
    get_recent_videos,
    count_videos_by_channel,
    count_videos_in_timerange
)
import json

def get_database_tools():
    """Return list of tools for Gemini function calling"""
    
    tools = [
        {
            "name": "get_recent_videos",
            "description": "Get the most recent videos from the database. Use this when user asks about recent videos, latest uploads, or newest content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Number of videos to retrieve (default: 10, max: 50)"
                    }
                },
                "required": []
            }
        },
        {
            "name": "count_videos_by_channel",
            "description": "Count total number of videos from a specific channel. Use when user asks how many videos a channel has.",
            "parameters": {
                "type": "object",
                "properties": {
                    "channel_name": {
                        "type": "string",
                        "description": "Name of the YouTube channel (can be partial match, e.g., 'ANI', 'REPORTER', 'Bloomberg')"
                    }
                },
                "required": ["channel_name"]
            }
        },
        {
            "name": "count_videos_in_timerange",
            "description": "Count videos uploaded in the last X hours for a channel. Use when user asks about recent uploads in a time period.",
            "parameters": {
                "type": "object",
                "properties": {
                    "channel_name": {
                        "type": "string",
                        "description": "Name of the channel"
                    },
                    "hours": {
                        "type": "integer",
                        "description": "Number of hours to look back"
                    }
                },
                "required": ["channel_name", "hours"]
            }
        }
    ]
    
    return tools

def execute_tool(tool_name: str, parameters: dict):
    """Execute a tool function and return results"""
    
    if tool_name == "get_recent_videos":
        limit = parameters.get("limit", 10)
        videos = get_recent_videos(limit)
        
        # Format for display
        result = f"Found {len(videos)} recent videos:\n\n"
        for i, video in enumerate(videos[:5], 1):  # Show top 5
            result += f"{i}. {video['title']}\n"
            result += f"   Channel: {video['channel_title']}\n"
            result += f"   Views: {video['view_count']:,} | Likes: {video['like_count']:,}\n"
            result += f"   URL: {video['url']}\n\n"
        
        return result
    
    elif tool_name == "count_videos_by_channel":
        channel_name = parameters.get("channel_name", "")
        count = count_videos_by_channel(channel_name)
        return f"Found {count} videos from '{channel_name}' channel."
    
    elif tool_name == "count_videos_in_timerange":
        channel_name = parameters.get("channel_name", "")
        hours = parameters.get("hours", 24)
        count = count_videos_in_timerange(channel_name, hours)
        return f"Found {count} videos from '{channel_name}' uploaded in the last {hours} hours."
    
    else:
        return f"Unknown tool: {tool_name}"
