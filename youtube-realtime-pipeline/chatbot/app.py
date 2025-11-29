import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from database.query_operations import get_recent_videos, count_videos_by_channel

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="YouTube Analytics Chatbot", page_icon="📺")
st.title("📺 YouTube Analytics AI Chatbot")
st.caption("Ask me about the YouTube videos in our database!")

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
        # Simple keyword-based responses
        response = ""
        
        if "how many" in prompt.lower() or "count" in prompt.lower():
            count = count_videos_by_channel("REPORTER")
            response = f"We have **{count} videos** in our database from REPORTER channel."
        
        elif "recent" in prompt.lower() or "latest" in prompt.lower():
            videos = get_recent_videos(5)
            response = f"### 🎬 Recent Videos:\n\n"
            for i, video in enumerate(videos, 1):
                response += f"**{i}. {video['title']}**\n"
                response += f"   - Channel: {video['channel_title']}\n"
                response += f"   - Views: {video['view_count']:,} 👁️\n"
                response += f"   - Likes: {video['like_count']:,} 👍\n"
                response += f"   - [Watch Video]({video['url']})\n\n"
        
        elif "help" in prompt.lower():
            response = """I can help you with:
            
- **"How many videos?"** - Get total video count
- **"Show recent videos"** - See latest uploads
- **"Latest videos"** - Same as above

Try asking one of these questions!"""
        
        else:
            # Use Gemini for general questions
            try:
                context = f"You are a YouTube analytics assistant. We have 133 videos in our database. User asked: {prompt}"
                gemini_response = model.generate_content(context)
                response = gemini_response.text
            except:
                response = "I can help you with video counts and recent videos. Try asking 'How many videos?' or 'Show recent videos'"
        
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
