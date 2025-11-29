from fastapi import FastAPI, Request, HTTPException
from database.mongodb_client import get_database
from data_ingestion.youtube_api import fetch_video_metadata
import xml.etree.ElementTree as ET
from datetime import datetime
import hashlib

app = FastAPI()

@app.get("/webhook")
async def verify_subscription(request: Request):
    """Verify PubSubHubbub subscription"""
    challenge = request.query_params.get("hub.challenge")
    mode = request.query_params.get("hub.mode")
    
    if mode == "subscribe":
        return challenge
    return HTTPException(status_code=400)

@app.post("/webhook")
async def receive_notification(request: Request):
    """Receive YouTube video notifications"""
    body = await request.body()
    xml_content = body.decode('utf-8')
    
    # Parse Atom feed
    root = ET.fromstring(xml_content)
    ns = {'yt': 'http://www.youtube.com/xml/schemas/2015',
          'atom': 'http://www.w3.org/2005/Atom'}
    
    video_id = root.find('.//yt:videoId', ns).text
    channel_id = root.find('.//yt:channelId', ns).text
    
    # Fetch complete metadata using YouTube Data API
    metadata = await fetch_video_metadata(video_id)
    
    # Store in MongoDB with idempotency
    db = get_database()
    collection = db['videos']
    
    # Use video_id as unique identifier for idempotency
    await collection.update_one(
        {"video_id": video_id},
        {"$set": metadata},
        upsert=True
    )
    
    return {"status": "success", "video_id": video_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
