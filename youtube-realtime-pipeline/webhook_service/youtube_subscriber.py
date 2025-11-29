import httpx
import asyncio

async def subscribe_to_channel(channel_id: str, callback_url: str):
    """Subscribe to YouTube channel using PubSubHubbub"""
    hub_url = "https://pubsubhubbub.appspot.com/subscribe"
    topic_url = f"https://www.youtube.com/xml/feeds/videos.xml?channel_id={channel_id}"
    
    data = {
        "hub.callback": callback_url,
        "hub.topic": topic_url,
        "hub.mode": "subscribe",
        "hub.verify": "async",
        "hub.lease_seconds": 864000  # 10 days
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(hub_url, data=data)
        return response.status_code == 202

# Subscribe to required channels
channels = [
    "UCnKJeK_r90jDdIuzHXC0Org",  # markets (Bloomberg)
    "UCFx1nseXKTc1Culiu3neeSQ",  # ANINewsIndia
]
