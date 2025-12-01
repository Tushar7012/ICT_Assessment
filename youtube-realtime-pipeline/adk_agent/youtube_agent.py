import google.generativeai as genai
import os
from typing import Dict, List, Any, Optional
from database.mongodb_client import get_sync_database

# Try to import function calling (may not be available in all accounts)
try:
    from google.generativeai.types import FunctionDeclaration, Tool
    HAS_FUNCTION_CALLING = True
except ImportError:
    HAS_FUNCTION_CALLING = False

import json

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class YouTubeADKAgent:
    """Production-grade AI Agent using Google ADK with function calling"""
    
    def __init__(self):
        self.db = get_sync_database()
        
        # Try to initialize with function calling, fallback to simple mode
        try:
            if HAS_FUNCTION_CALLING:
                # Define tools with proper schema (ADK requirement)
                self.tools = self._define_tools()
                
                # Initialize model with function calling - USE GEMINI-PRO
                self.model = genai.GenerativeModel(
                    model_name='gemini-pro',  # CHANGED FROM gemini-1.5-flash
                    tools=[self.tools]
                )
                
                # Start chat session for multi-turn conversations
                self.chat = self.model.start_chat()
                self.use_function_calling = True
            else:
                raise Exception("Function calling not available")
        except Exception as e:
            # Fallback to simple mode
            print(f"Function calling not available, using fallback mode: {e}")
            self.model = genai.GenerativeModel('gemini-pro')
            self.use_function_calling = False
    
    def _define_tools(self) -> Tool:
        """
        Define tools with proper schema definition (ADK standard)
        This enables automatic tool orchestration
        """
        if not HAS_FUNCTION_CALLING:
            return None
        
        get_video_stats_func = FunctionDeclaration(
            name="get_video_stats",
            description="Get total count of videos in the database. Use this when user asks about total videos, how many videos, or database size.",
            parameters={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
        
        get_recent_videos_func = FunctionDeclaration(
            name="get_recent_videos",
            description="Retrieve the most recent videos from database. Use when user asks for recent, latest, or new videos.",
            parameters={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Number of videos to retrieve (default: 5, max: 20)"
                    }
                },
                "required": []
            }
        )
        
        search_videos_func = FunctionDeclaration(
            name="search_videos",
            description="Search for videos by keyword in title or description. Use when user wants to find specific content.",
            parameters={
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "Search keyword or phrase"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results (default: 10)"
                    }
                },
                "required": ["keyword"]
            }
        )
        
        get_channel_stats_func = FunctionDeclaration(
            name="get_channel_stats",
            description="Get detailed statistics for a specific YouTube channel including video count, total views, and engagement metrics.",
            parameters={
                "type": "object",
                "properties": {
                    "channel_name": {
                        "type": "string",
                        "description": "Name of the channel (e.g., 'REPORTER', 'ANI News')"
                    }
                },
                "required": ["channel_name"]
            }
        )
        
        get_trending_videos_func = FunctionDeclaration(
            name="get_trending_videos",
            description="Get trending videos sorted by view count. Use when user asks about popular, trending, or most viewed videos.",
            parameters={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Number of trending videos to retrieve (default: 5)"
                    }
                },
                "required": []
            }
        )
        
        compare_channels_func = FunctionDeclaration(
            name="compare_channels",
            description="Compare statistics between multiple channels. Use for comparative analysis.",
            parameters={
                "type": "object",
                "properties": {
                    "channels": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of channel names to compare"
                    }
                },
                "required": ["channels"]
            }
        )
        
        # Create Tool object with all functions
        return Tool(function_declarations=[
            get_video_stats_func,
            get_recent_videos_func,
            search_videos_func,
            get_channel_stats_func,
            get_trending_videos_func,
            compare_channels_func
        ])
    
    # ========== TOOL IMPLEMENTATIONS ==========
    
    def get_video_stats(self) -> Dict[str, Any]:
        """Tool: Get total video statistics"""
        try:
            total = self.db.videos.count_documents({})
            channels = self.db.videos.distinct("channelTitle")
            
            return {
                "total_videos": total,
                "total_channels": len(channels),
                "channels": channels,
                "status": "success"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_recent_videos(self, limit: int = 5) -> Dict[str, Any]:
        """Tool: Get recent videos with validation"""
        try:
            limit = min(max(limit, 1), 20)
            videos = list(self.db.videos.find().sort("publishedAt", -1).limit(limit))
            
            results = []
            for v in videos:
                results.append({
                    "title": v.get("title", "N/A"),
                    "channel": v.get("channelTitle", "N/A"),
                    "views": v.get("viewCount", 0),
                    "likes": v.get("likeCount", 0),
                    "published": str(v.get("publishedAt", "N/A")),
                    "url": v.get("url", "")
                })
            
            return {
                "status": "success",
                "count": len(results),
                "videos": results
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def search_videos(self, keyword: str, limit: int = 10) -> Dict[str, Any]:
        """Tool: Search videos by keyword with validation"""
        try:
            if not keyword or len(keyword.strip()) < 2:
                return {
                    "status": "error",
                    "message": "Keyword must be at least 2 characters"
                }
            
            limit = min(max(limit, 1), 50)
            videos = list(self.db.videos.find(
                {"title": {"$regex": keyword, "$options": "i"}}
            ).limit(limit))
            
            results = []
            for v in videos:
                results.append({
                    "title": v.get("title", "N/A"),
                    "channel": v.get("channelTitle", "N/A"),
                    "views": v.get("viewCount", 0),
                    "url": v.get("url", "")
                })
            
            return {
                "status": "success",
                "keyword": keyword,
                "count": len(results),
                "videos": results
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_channel_stats(self, channel_name: str) -> Dict[str, Any]:
        """Tool: Get channel statistics with validation"""
        try:
            if not channel_name:
                return {"status": "error", "message": "Channel name required"}
            
            videos = list(self.db.videos.find({"channelTitle": channel_name}))
            
            if not videos:
                all_channels = self.db.videos.distinct("channelTitle")
                matches = [c for c in all_channels if channel_name.lower() in c.lower()]
                
                return {
                    "status": "not_found",
                    "message": f"Channel '{channel_name}' not found",
                    "suggestions": matches
                }
            
            total_views = sum(v.get("viewCount", 0) for v in videos)
            total_likes = sum(v.get("likeCount", 0) for v in videos)
            
            return {
                "status": "success",
                "channel": channel_name,
                "total_videos": len(videos),
                "total_views": total_views,
                "total_likes": total_likes,
                "avg_views": total_views // len(videos) if videos else 0,
                "avg_likes": total_likes // len(videos) if videos else 0
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_trending_videos(self, limit: int = 5) -> Dict[str, Any]:
        """Tool: Get trending videos sorted by views"""
        try:
            limit = min(max(limit, 1), 20)
            videos = list(self.db.videos.find().sort("viewCount", -1).limit(limit))
            
            results = []
            for v in videos:
                results.append({
                    "title": v.get("title", "N/A"),
                    "channel": v.get("channelTitle", "N/A"),
                    "views": v.get("viewCount", 0),
                    "likes": v.get("likeCount", 0),
                    "url": v.get("url", "")
                })
            
            return {
                "status": "success",
                "count": len(results),
                "videos": results
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def compare_channels(self, channels: List[str]) -> Dict[str, Any]:
        """Tool: Compare multiple channels"""
        try:
            if not channels or len(channels) < 2:
                return {
                    "status": "error",
                    "message": "Need at least 2 channels to compare"
                }
            
            comparison = {}
            for channel in channels:
                stats = self.get_channel_stats(channel)
                if stats.get("status") == "success":
                    comparison[channel] = stats
            
            return {
                "status": "success",
                "comparison": comparison,
                "channels_compared": len(comparison)
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    # ========== FORMATTING ==========
    
    def _format_response(self, data: Dict, query_type: str) -> str:
        """Format tool responses for display"""
        if query_type == "stats":
            if data.get("status") == "success":
                channels_str = ", ".join(data["channels"])
                return f"📊 **Database Stats:**\n\nTotal Videos: **{data['total_videos']}**\nChannels: {channels_str}"
            return f"Error: {data.get('message')}"
        
        elif query_type == "recent":
            if data.get("status") == "success":
                result = f"### 🎬 Recent Videos:\n\n"
                for i, v in enumerate(data["videos"], 1):
                    result += f"**{i}. {v['title']}**\n   - {v['channel']} | {v['views']:,} views\n\n"
                return result
            return f"Error: {data.get('message')}"
        
        elif query_type == "search":
            if data.get("status") == "success":
                if data["count"] == 0:
                    return f"No videos found for '{data['keyword']}'"
                result = f"### 🔍 Found {data['count']} videos:\n\n"
                for i, v in enumerate(data["videos"], 1):
                    result += f"**{i}. {v['title']}**\n   - {v['views']:,} views\n\n"
                return result
            return f"Error: {data.get('message')}"
        
        elif query_type == "channel":
            if data.get("status") == "success":
                return f"### 📺 {data['channel']}:\n\nVideos: **{data['total_videos']}**\nTotal Views: **{data['total_views']:,}**\nAvg Views: **{data['avg_views']:,}**"
            return f"Error: {data.get('message')}"
        
        elif query_type == "trending":
            if data.get("status") == "success":
                result = f"### 🔥 Trending Videos:\n\n"
                for i, v in enumerate(data["videos"], 1):
                    result += f"**{i}. {v['title']}**\n   - {v['views']:,} views\n\n"
                return result
            return f"Error: {data.get('message')}"
        
        return str(data)
    
    # ========== TOOL ORCHESTRATION ==========
    
    def _execute_function(self, function_call) -> Any:
        """Execute function calls from the model"""
        function_name = function_call.name
        function_args = {}
        
        if function_call.args:
            function_args = dict(function_call.args)
        
        try:
            if function_name == "get_video_stats":
                return self.get_video_stats()
            elif function_name == "get_recent_videos":
                limit = function_args.get("limit", 5)
                return self.get_recent_videos(limit)
            elif function_name == "search_videos":
                keyword = function_args.get("keyword", "")
                limit = function_args.get("limit", 10)
                return self.search_videos(keyword, limit)
            elif function_name == "get_channel_stats":
                channel = function_args.get("channel_name", "")
                return self.get_channel_stats(channel)
            elif function_name == "get_trending_videos":
                limit = function_args.get("limit", 5)
                return self.get_trending_videos(limit)
            elif function_name == "compare_channels":
                channels = function_args.get("channels", [])
                return self.compare_channels(channels)
            else:
                return {"status": "error", "message": f"Unknown function: {function_name}"}
        except Exception as e:
            return {"status": "error", "function": function_name, "message": str(e)}
    
    # ========== FALLBACK ROUTING ==========
    
    def _fallback_query(self, user_input: str) -> str:
        """Fallback query handling without function calling"""
        user_lower = user_input.lower()
        
        if any(word in user_lower for word in ["how many", "total", "count"]):
            data = self.get_video_stats()
            return self._format_response(data, "stats")
        
        elif any(word in user_lower for word in ["recent", "latest"]):
            data = self.get_recent_videos(5)
            return self._format_response(data, "recent")
        
        elif any(word in user_lower for word in ["trending", "popular"]):
            data = self.get_trending_videos(5)
            return self._format_response(data, "trending")
        
        elif any(word in user_lower for word in ["search", "find", "about"]):
            words = user_input.split()
            keyword = words[-1] if words else "news"
            data = self.search_videos(keyword, 10)
            return self._format_response(data, "search")
        
        elif any(word in user_lower for word in ["channel", "reporter", "ani"]):
            channel = "REPORTER" if "reporter" in user_lower else "ANI News"
            data = self.get_channel_stats(channel)
            return self._format_response(data, "channel")
        
        elif "compare" in user_lower:
            data = self.compare_channels(["REPORTER", "ANI News"])
            return str(data)
        
        else:
            prompt = f"User asked: {user_input}\n\nSuggest what they can ask about a YouTube video database."
            response = self.model.generate_content(prompt)
            return response.text
    
    # ========== MAIN QUERY METHOD ==========
    
    def query(self, user_input: str, max_iterations: int = 5) -> str:
        """Main query with automatic fallback"""
        try:
            # If function calling is available, use it
            if self.use_function_calling:
                try:
                    response = self.chat.send_message(user_input)
                    iteration = 0
                    
                    while iteration < max_iterations:
                        if hasattr(response.candidates[0].content.parts[0], 'function_call') and response.candidates[0].content.parts[0].function_call:
                            function_call = response.candidates[0].content.parts[0].function_call
                            function_result = self._execute_function(function_call)
                            
                            response = self.chat.send_message(
                                genai.protos.Content(
                                    parts=[genai.protos.Part(
                                        function_response=genai.protos.FunctionResponse(
                                            name=function_call.name,
                                            response={'result': function_result}
                                        )
                                    )]
                                )
                            )
                            iteration += 1
                        else:
                            break
                    
                    return response.text
                except Exception as e:
                    # Fall back to simple routing
                    print(f"Function calling failed, using fallback: {e}")
                    return self._fallback_query(user_input)
            else:
                # Use fallback routing
                return self._fallback_query(user_input)
        
        except Exception as e:
            error_message = f"⚠️ Error: {str(e)}\n\nTry: 'How many videos?', 'Show recent videos', 'REPORTER channel stats'"
            return error_message

# Create agent instance
agent = YouTubeADKAgent()
