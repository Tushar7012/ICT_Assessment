import google.generativeai as genai
import os
from database.mongodb_client import get_sync_database

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class YouTubeAgent:
    """AI Agent for YouTube Analytics using Google Gemini"""
    
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.db = get_sync_database()
        
    def get_video_stats(self):
        """Tool: Get total video statistics"""
        total = self.db.videos.count_documents({})
        return f"Total videos in database: {total}"
    
    def get_recent_videos(self, limit=5):
        """Tool: Get recent videos"""
        videos = list(self.db.videos.find().sort("publishedAt", -1).limit(limit))
        result = []
        for v in videos:
            result.append({
                "title": v.get("title", "N/A"),
                "channel": v.get("channelTitle", "N/A"),
                "views": v.get("viewCount", 0),
                "published": str(v.get("publishedAt", "N/A"))
            })
        return result
    
    def search_videos(self, keyword):
        """Tool: Search videos by keyword"""
        videos = list(self.db.videos.find(
            {"title": {"$regex": keyword, "$options": "i"}}
        ).limit(10))
        return len(videos), [v.get("title") for v in videos]
    
    def get_channel_stats(self, channel_name):
        """Tool: Get channel statistics"""
        count = self.db.videos.count_documents({"channelTitle": channel_name})
        videos = list(self.db.videos.find({"channelTitle": channel_name}))
        total_views = sum(v.get("viewCount", 0) for v in videos)
        return {
            "channel": channel_name,
            "total_videos": count,
            "total_views": total_views
        }
    
    def query(self, user_input):
        """Main agent query method"""
        # Prepare context with available tools
        context = """
You are a YouTube Analytics Agent with access to a database of videos.

Available tools:
1. get_video_stats() - Get total count of videos
2. get_recent_videos(limit) - Get recent videos
3. search_videos(keyword) - Search videos by keyword
4. get_channel_stats(channel_name) - Get channel statistics

Current database stats: """ + self.get_video_stats()
        
        # Detect intent and call appropriate tool
        user_lower = user_input.lower()
        
        if "how many" in user_lower or "total" in user_lower or "count" in user_lower:
            data = self.get_video_stats()
            prompt = f"{context}\n\nUser asked: {user_input}\nData: {data}\n\nProvide a helpful response."
            
        elif "recent" in user_lower or "latest" in user_lower:
            data = self.get_recent_videos(5)
            prompt = f"{context}\n\nUser asked: {user_input}\nRecent videos: {data}\n\nProvide a formatted response."
            
        elif "search" in user_lower or "find" in user_lower:
            # Extract keyword (simplified)
            keyword = user_input.split()[-1]
            count, titles = self.search_videos(keyword)
            prompt = f"{context}\n\nUser asked: {user_input}\nFound {count} videos matching '{keyword}': {titles[:5]}\n\nProvide a helpful response."
            
        elif "channel" in user_lower:
            # Extract channel name (simplified)
            words = user_input.split()
            channel = words[-1] if len(words) > 1 else "REPORTER"
            stats = self.get_channel_stats(channel)
            prompt = f"{context}\n\nUser asked: {user_input}\nChannel stats: {stats}\n\nProvide a formatted response."
            
        else:
            prompt = f"{context}\n\nUser asked: {user_input}\n\nProvide a helpful response based on available tools."
        
        # Generate response
        response = self.model.generate_content(prompt)
        return response.text

# Create agent instance
agent = YouTubeAgent()
