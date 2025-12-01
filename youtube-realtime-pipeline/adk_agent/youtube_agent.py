import google.generativeai as genai
import os
from typing import Dict, Any, List
from database.mongodb_client import get_sync_database

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class YouTubeADKAgent:
    """
    Production-grade AI Agent for YouTube Analytics
    Features:
    - Tool-based architecture
    - Input validation
    - Error handling
    - Multi-tool orchestration
    """
    
    def __init__(self):
        """Initialize agent with database connection and AI model"""
        try:
            self.db = get_sync_database()
            # Use gemini-pro (most stable and widely available)
            self.model = genai.GenerativeModel('gemini-pro')
            self.initialized = True
        except Exception as e:
            print(f"Agent initialization error: {e}")
            self.initialized = False
    
    # ========== TOOL IMPLEMENTATIONS ==========
    
    def get_video_stats(self) -> Dict[str, Any]:
        """
        Tool: Get total video statistics
        Returns: Dictionary with total count and channel list
        """
        try:
            total = self.db.videos.count_documents({})
            channels = self.db.videos.distinct("channelTitle")
            
            return {
                "status": "success",
                "total_videos": total,
                "total_channels": len(channels),
                "channels": channels
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    def get_recent_videos(self, limit: int = 5) -> str:
        """
        Tool: Get recent videos with formatting
        Args:
            limit: Number of videos to retrieve (1-20)
        Returns: Formatted string with video list
        """
        try:
            # Input validation
            limit = min(max(int(limit), 1), 20)
            
            videos = list(self.db.videos.find().sort("publishedAt", -1).limit(limit))
            
            if not videos:
                return "No videos found in database."
            
            result = f"### 🎬 {limit} Most Recent Videos:\n\n"
            
            for i, v in enumerate(videos, 1):
                title = v.get('title', 'N/A')
                channel = v.get('channelTitle', 'N/A')
                views = v.get('viewCount', 0)
                likes = v.get('likeCount', 0)
                url = v.get('url', '#')
                
                result += f"**{i}. {title}**\n"
                result += f"   - 📺 Channel: {channel}\n"
                result += f"   - 👁️ Views: {views:,} | 👍 Likes: {likes:,}\n"
                result += f"   - 🔗 [Watch Video]({url})\n\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving recent videos: {str(e)}"
    
    def search_videos(self, keyword: str, limit: int = 10) -> str:
        """
        Tool: Search videos by keyword
        Args:
            keyword: Search term
            limit: Max results (1-50)
        Returns: Formatted search results
        """
        try:
            # Input validation
            if not keyword or len(keyword.strip()) < 2:
                return "❌ Please provide a search keyword (at least 2 characters)"
            
            limit = min(max(int(limit), 1), 50)
            
            # Case-insensitive regex search
            videos = list(self.db.videos.find(
                {"title": {"$regex": keyword, "$options": "i"}}
            ).limit(limit))
            
            if not videos:
                return f"No videos found matching '{keyword}'\n\nTry searching for: news, India, live, reporter"
            
            result = f"### 🔍 Found {len(videos)} videos about '{keyword}':\n\n"
            
            for i, v in enumerate(videos, 1):
                title = v.get('title', 'N/A')
                channel = v.get('channelTitle', 'N/A')
                views = v.get('viewCount', 0)
                url = v.get('url', '#')
                
                result += f"**{i}. {title}**\n"
                result += f"   - Channel: {channel}\n"
                result += f"   - Views: {views:,}\n"
                result += f"   - [Watch]({url})\n\n"
            
            return result
            
        except Exception as e:
            return f"Error searching videos: {str(e)}"
    
    def get_channel_stats(self, channel_name: str) -> str:
        """
        Tool: Get comprehensive channel statistics
        Args:
            channel_name: Name of the channel
        Returns: Formatted channel statistics
        """
        try:
            if not channel_name or len(channel_name.strip()) < 2:
                return "❌ Please provide a valid channel name"
            
            # Find all videos from this channel
            videos = list(self.db.videos.find({"channelTitle": channel_name}))
            
            if not videos:
                # Try to suggest similar channels
                all_channels = self.db.videos.distinct("channelTitle")
                suggestions = [c for c in all_channels if channel_name.lower() in c.lower()]
                
                if suggestions:
                    return f"Channel '{channel_name}' not found.\n\n**Did you mean:** {', '.join(suggestions)}"
                else:
                    return f"Channel '{channel_name}' not found.\n\n**Available channels:** {', '.join(all_channels)}"
            
            # Calculate statistics
            total_views = sum(v.get("viewCount", 0) for v in videos)
            total_likes = sum(v.get("likeCount", 0) for v in videos)
            total_comments = sum(v.get("commentCount", 0) for v in videos)
            
            avg_views = total_views // len(videos) if videos else 0
            avg_likes = total_likes // len(videos) if videos else 0
            
            # Get most viewed video
            most_viewed = max(videos, key=lambda x: x.get('viewCount', 0))
            
            result = f"### 📺 {channel_name} Channel Statistics:\n\n"
            result += f"**Overview:**\n"
            result += f"- Total Videos: **{len(videos)}**\n"
            result += f"- Total Views: **{total_views:,}**\n"
            result += f"- Total Likes: **{total_likes:,}**\n"
            result += f"- Total Comments: **{total_comments:,}**\n\n"
            
            result += f"**Averages:**\n"
            result += f"- Avg Views per Video: **{avg_views:,}**\n"
            result += f"- Avg Likes per Video: **{avg_likes:,}**\n\n"
            
            result += f"**Most Popular Video:**\n"
            result += f"- Title: {most_viewed.get('title', 'N/A')}\n"
            result += f"- Views: {most_viewed.get('viewCount', 0):,}\n"
            
            return result
            
        except Exception as e:
            return f"Error getting channel stats: {str(e)}"
    
    def get_trending_videos(self, limit: int = 5) -> str:
        """
        Tool: Get trending videos (sorted by views)
        Args:
            limit: Number of videos (1-20)
        Returns: Formatted trending videos list
        """
        try:
            limit = min(max(int(limit), 1), 20)
            
            videos = list(self.db.videos.find().sort("viewCount", -1).limit(limit))
            
            if not videos:
                return "No videos found in database."
            
            result = f"### 🔥 Top {limit} Trending Videos (Most Views):\n\n"
            
            for i, v in enumerate(videos, 1):
                title = v.get('title', 'N/A')
                channel = v.get('channelTitle', 'N/A')
                views = v.get('viewCount', 0)
                likes = v.get('likeCount', 0)
                url = v.get('url', '#')
                
                result += f"**{i}. {title}**\n"
                result += f"   - Channel: {channel}\n"
                result += f"   - 👁️ **{views:,}** views | 👍 {likes:,} likes\n"
                result += f"   - [Watch]({url})\n\n"
            
            return result
            
        except Exception as e:
            return f"Error getting trending videos: {str(e)}"
    
    def compare_channels(self, channels: List[str]) -> str:
        """
        Tool: Compare statistics between multiple channels
        Args:
            channels: List of channel names to compare
        Returns: Comparative analysis
        """
        try:
            if not channels or len(channels) < 2:
                return "❌ Please provide at least 2 channels to compare"
            
            result = "### 🔍 Channel Comparison:\n\n"
            
            for channel in channels:
                stats = self.get_channel_stats(channel)
                result += f"{stats}\n\n---\n\n"
            
            return result
            
        except Exception as e:
            return f"Error comparing channels: {str(e)}"
    
    # ========== MAIN QUERY METHOD ==========
    
    def query(self, user_input: str) -> str:
        """
        Main query handler with intelligent routing
        
        Features:
        - Automatic tool selection based on query analysis
        - Multi-tool orchestration for complex queries
        - Error handling and fallback responses
        - AI-powered responses for ambiguous queries
        
        Args:
            user_input: Natural language query from user
            
        Returns:
            Formatted response string
        """
        
        if not self.initialized:
            return "⚠️ Agent not initialized properly. Please check database connection."
        
        try:
            user_lower = user_input.lower()
            
            # ===== TOOL ROUTING LOGIC =====
            
            # Video Count Query
            if any(word in user_lower for word in ["how many", "total", "count", "number of"]):
                stats = self.get_video_stats()
                if stats["status"] == "success":
                    channels_str = ", ".join(stats["channels"])
                    return f"📊 **Database Statistics:**\n\nWe have **{stats['total_videos']} videos** from **{stats['total_channels']} channels**:\n\n{channels_str}"
                else:
                    return f"Error: {stats['message']}"
            
            # Recent Videos Query
            elif any(word in user_lower for word in ["recent", "latest", "new"]):
                return self.get_recent_videos(5)
            
            # Trending Videos Query
            elif any(word in user_lower for word in ["trending", "popular", "most viewed", "top"]):
                return self.get_trending_videos(5)
            
            # Search Query
            elif any(word in user_lower for word in ["search", "find", "about", "videos on"]):
                # Extract keyword
                stop_words = ["search", "find", "videos", "about", "for", "me", "on", "the", "show"]
                words = user_input.lower().split()
                keyword = None
                
                for word in words:
                    if word not in stop_words and len(word) > 2:
                        keyword = word
                        break
                
                if keyword:
                    return self.search_videos(keyword, 10)
                else:
                    return "Please specify what to search for.\n\nExample: 'Find videos about news' or 'Search for India'"
            
            # Channel Statistics Query
            elif any(word in user_lower for word in ["channel", "reporter", "ani"]):
                if "reporter" in user_lower:
                    return self.get_channel_stats("REPORTER")
                elif "ani" in user_lower:
                    return self.get_channel_stats("ANI News")
                else:
                    return "Which channel would you like stats for?\n\nAvailable: REPORTER, ANI News"
            
            # Comparison Query
            elif "compare" in user_lower:
                channels = ["REPORTER", "ANI News"]
                return self.compare_channels(channels)
            
            # Help Query
            elif "help" in user_lower:
                return """### 💡 What I Can Help You With:
                
**📊 Statistics:**
- "How many videos do we have?"
- "Total videos in database"

**🎬 Video Lists:**
- "Show me recent videos"
- "Latest uploads"

**🔥 Trending:**
- "What are the trending videos?"
- "Most popular videos"

**🔍 Search:**
- "Find videos about [keyword]"
- "Search for [topic]"

**📺 Channel Info:**
- "Tell me about REPORTER channel"
- "ANI channel statistics"

**🔄 Comparison:**
- "Compare REPORTER and ANI channels"

Try any of these questions!"""
            
            # AI-Powered Response for Complex/Ambiguous Queries
            else:
                context = f"""You are a YouTube analytics assistant.

Database Info:
- We have 133+ videos from news channels like REPORTER and ANI News
- Videos cover news, current affairs, and breaking news

User Query: {user_input}

Provide a helpful 2-3 sentence response. If the query is unclear, suggest what they can ask about from the available tools:
- Video counts
- Recent videos
- Trending videos
- Search by keyword
- Channel statistics
"""
                
                response = self.model.generate_content(context)
                return response.text
        
        except Exception as e:
            # Production-grade error handling
            error_msg = f"⚠️ An error occurred: {str(e)}\n\n"
            error_msg += "**Try these queries:**\n"
            error_msg += "- How many videos do we have?\n"
            error_msg += "- Show me recent videos\n"
            error_msg += "- Tell me about REPORTER channel\n"
            error_msg += "- Find videos about news\n"
            
            return error_msg

# Create global agent instance
agent = YouTubeADKAgent()
