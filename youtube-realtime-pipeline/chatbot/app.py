import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from database.query_operations import get_recent_videos, count_videos_by_channel, get_channel_statistics
from database.mongodb_client import get_sync_database

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(
    page_title="YouTube Analytics AI",
    page_icon="📺",
    layout="wide"
)

# Sidebar with stats
with st.sidebar:
    st.title("📊 Database Stats")
    try:
        db = get_sync_database()
        total_videos = db['videos'].count_documents({})
        st.metric("Total Videos", total_videos)
        
        reporter_count = count_videos_by_channel("REPORTER")
        st.metric("REPORTER Channel", reporter_count)
        
        st.divider()
        st.subheader("💡 Try Asking")
        st.markdown("""
        - How many videos?
        - Show recent videos
        - Trending videos
        - About REPORTER channel
        - What kind of videos?
        """)
    except:
        st.error("Database connection failed")

# Main interface
st.title("🎥 YouTube Analytics AI Assistant")
st.caption("Ask me anything about the video database!")

# Initialize chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about videos..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response = ""
        prompt_lower = prompt.lower()
        
        # Keyword detection - Video Count
        if any(word in prompt_lower for word in ["how many", "total", "count", "number of"]):
            try:
                db = get_sync_database()
                count = db['videos'].count_documents({})
                response = f"📊 We have **{count} videos** in our database from various YouTube news channels!"
            except:
                response = "Unable to fetch video count from database."
        
        # Recent/Latest Videos
        elif any(word in prompt_lower for word in ["recent", "latest", "new"]):
            videos = get_recent_videos(5)
            response = "### 🎬 Latest Videos:\n\n"
            for i, video in enumerate(videos, 1):
                response += f"**{i}. {video['title']}**\n"
                response += f"   - 📺 Channel: {video['channel_title']}\n"
                response += f"   - 👁️ {video['view_count']:,} views | 👍 {video['like_count']:,} likes\n"
                response += f"   - 🔗 [Watch Video]({video['url']})\n\n"
        
        # Trending/Popular Videos
        elif any(word in prompt_lower for word in ["trending", "popular", "most viewed", "top"]):
            try:
                db = get_sync_database()
                cursor = db['videos'].find().sort("view_count", -1).limit(5)
                videos = list(cursor)
                
                response = "### 🔥 Trending Videos (Most Views):\n\n"
                for i, video in enumerate(videos, 1):
                    video['_id'] = str(video['_id'])
                    response += f"**{i}. {video['title']}**\n"
                    response += f"   - 👁️ **{video['view_count']:,}** views\n"
                    response += f"   - 📺 {video['channel_title']}\n"
                    response += f"   - 🔗 [Watch]({video['url']})\n\n"
            except:
                response = "Unable to fetch trending videos."
        
        # Channel Statistics
        elif any(word in prompt_lower for word in ["channel", "reporter", "ani"]):
            channel_name = "REPORTER"
            stats = get_channel_statistics(channel_name)
            if stats:
                response = f"### 📺 {channel_name} Channel Statistics:\n\n"
                response += f"- **Total Videos:** {stats['total_videos']}\n"
                response += f"- **Total Views:** {stats['total_views']:,}\n"
                response += f"- **Total Likes:** {stats['total_likes']:,}\n"
                response += f"- **Average Views per Video:** {stats['avg_views']:,.0f}\n"
                response += f"- **Average Likes per Video:** {stats['avg_likes']:,.0f}\n"
            else:
                response = "Channel data not found."
        
        # What kind of videos - Shows actual data
        elif any(word in prompt_lower for word in ["what kind", "type", "category", "about videos", "describe"]):
            try:
                db = get_sync_database()
                
                # Get channel distribution
                pipeline = [
                    {"$group": {"_id": "$channel_title", "count": {"$sum": 1}}},
                    {"$sort": {"count": -1}}
                ]
                channel_stats = list(db['videos'].aggregate(pipeline))
                
                # Get sample videos
                sample_videos = list(db['videos'].find().limit(3))
                
                response = "### 📺 Video Database Overview:\n\n"
                response += f"Our database contains **133+ news videos** from the following channels:\n\n"
                
                for stat in channel_stats:
                    response += f"- **{stat['_id']}**: {stat['count']} videos\n"
                
                response += f"\n**Content Type:** News, current affairs, breaking news, and live updates\n\n"
                response += f"**Sample Video Titles:**\n"
                
                for i, video in enumerate(sample_videos, 1):
                    title = video['title'][:60] + "..." if len(video['title']) > 60 else video['title']
                    response += f"{i}. {title}\n"
                
                response += f"\n**Focus:** Indian and international news coverage with real-time updates from trusted sources. 📰"
                
            except Exception as e:
                response = "Our database contains **133+ news videos** from channels like **REPORTER LIVE** and **ANI News**, covering breaking news, current affairs, political updates, and events from India and around the world. 📰"
        
        # Help
        elif "help" in prompt_lower:
            response = """### I can help you with:

**📊 Statistics:**
- "How many videos do we have?"
- "Total videos in database"

**🎬 Video Lists:**
- "Show me recent videos"
- "Latest uploads"

**🔥 Trending:**
- "What are the trending videos?"
- "Most popular videos"

**📺 Channel Info:**
- "Tell me about REPORTER channel"
- "Channel statistics"

**📋 Content Overview:**
- "What kind of videos are in the database?"

Try any of these questions!"""
        
        # Default - Use AI
        else:
            try:
                context = f"""You are a YouTube analytics assistant. 
We have 133+ videos in our MongoDB database from news channels like REPORTER LIVE and ANI News.
The videos cover news, current affairs, breaking news, and updates.

User question: {prompt}

Provide a helpful, concise 2-3 sentence response. If you're not sure, suggest what the user can ask about."""
                
                gemini_response = model.generate_content(context)
                response = gemini_response.text
            except:
                response = """I can help you with:
- Video counts: "How many videos?"
- Recent content: "Show recent videos"
- Trending videos: "What's trending?"
- Channel info: "About REPORTER channel"
- Content overview: "What kind of videos?"

Try one of these questions!"""
        
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
