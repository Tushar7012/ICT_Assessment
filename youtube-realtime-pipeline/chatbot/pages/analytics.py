import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import streamlit as st
import pandas as pd
from database.mongodb_client import get_sync_database
import plotly.express as px

st.set_page_config(page_title="Analytics Dashboard", page_icon="📊", layout="wide")

st.title("📊 YouTube Analytics Dashboard")
st.caption("Real-time insights from your video database")

# Get data
db = get_sync_database()
videos = list(db['videos'].find().limit(100))

if videos:
    # Convert to DataFrame
    df = pd.DataFrame(videos)
    df['_id'] = df['_id'].astype(str)
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Videos", len(df))
    with col2:
        st.metric("Total Views", f"{df['view_count'].sum():,.0f}")
    with col3:
        st.metric("Total Likes", f"{df['like_count'].sum():,.0f}")
    with col4:
        st.metric("Avg Views/Video", f"{df['view_count'].mean():,.0f}")
    
    st.divider()
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📺 Top Channels by Video Count")
        channel_counts = df['channel_title'].value_counts().head(10)
        fig1 = px.bar(
            x=channel_counts.values,
            y=channel_counts.index,
            orientation='h',
            labels={'x': 'Number of Videos', 'y': 'Channel'},
            color=channel_counts.values,
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.subheader("🔥 Top Videos by Views")
        top_videos = df.nlargest(10, 'view_count')[['title', 'view_count']]
        top_videos['title_short'] = top_videos['title'].str[:40] + '...'
        fig2 = px.bar(
            top_videos,
            x='view_count',
            y='title_short',
            orientation='h',
            labels={'view_count': 'Views', 'title_short': 'Video'},
            color='view_count',
            color_continuous_scale='Reds'
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # Engagement metrics
    st.divider()
    st.subheader("📈 Engagement Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Like rate
        df['like_rate'] = (df['like_count'] / df['view_count'] * 100).round(2)
        top_engagement = df.nlargest(10, 'like_rate')[['title', 'like_rate', 'view_count']]
        st.write("**Top 10 Videos by Like Rate (%)**")
        st.dataframe(top_engagement, use_container_width=True)
    
    with col2:
        # Views distribution
        fig3 = px.histogram(
            df,
            x='view_count',
            nbins=30,
            title='Views Distribution',
            labels={'view_count': 'View Count'},
            color_discrete_sequence=['#1f77b4']
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    # Data table
    st.divider()
    st.subheader("🗂️ Raw Data Explorer")
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        selected_channel = st.selectbox("Filter by Channel", ["All"] + list(df['channel_title'].unique()))
    with col2:
        min_views = st.number_input("Minimum Views", min_value=0, value=0)
    
    filtered_df = df.copy()
    if selected_channel != "All":
        filtered_df = filtered_df[filtered_df['channel_title'] == selected_channel]
    filtered_df = filtered_df[filtered_df['view_count'] >= min_views]
    
    display_cols = ['title', 'channel_title', 'view_count', 'like_count', 'upload_date']
    st.dataframe(filtered_df[display_cols].head(50), use_container_width=True)
    
else:
    st.warning("No data available. Please run initial data load.")
