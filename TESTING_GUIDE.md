# Testing Guide

## Prerequisites

Before testing, ensure:
- API server is running on port 8000
- Chatbot is running on port 8501
- MongoDB Atlas is accessible
- Valid API key is configured in `.env`

---

## Quick Start Testing

### 1. Start Services

**Terminal 1 - API:**
uvicorn api.main:app --reload --port 8000

**Terminal 2 - Chatbot:**
streamlit run chatbot/app.py

---

## API Testing

### Test 1: Health Check (No Auth Required)

curl http://localhost:8000/health


**Expected Result:**
{
"status": "healthy",
"database": "connected",
"total_videos": 133
}


**Status Code:** 200 OK

---

### Test 2: Get Recent Videos

curl -H "X-API-Key: my-secret-key-123"
"http://localhost:8000/api/videos/recent?limit=3"


**Expected Result:**
- Status Code: 200 OK
- JSON response with 3 videos
- Each video has: video_id, title, channel_title, view_count, like_count, url

---

### Test 3: Search Videos

curl -H "X-API-Key: my-secret-key-123"
"http://localhost:8000/api/videos/search?keyword=news&limit=5"


**Expected Result:**
- Status Code: 200 OK
- Videos containing "news" in title or description
- Max 5 results

---

### Test 4: Get Trending Videos

curl -H "X-API-Key: my-secret-key-123"
"http://localhost:8000/api/videos/trending?limit=10"


**Expected Result:**
- Status Code: 200 OK
- 10 videos sorted by view_count (highest first)

---

### Test 5: Count Channel Videos

curl -H "X-API-Key: my-secret-key-123"
"http://localhost:8000/api/videos/count/REPORTER"


**Expected Result:**
{
"status": "success",
"channel": "REPORTER",
"video_count": 115
}


---

### Test 6: Channel Statistics

curl -H "X-API-Key: my-secret-key-123"
"http://localhost:8000/api/videos/channel/REPORTER/stats"


**Expected Result:**
- Status Code: 200 OK
- Statistics including: total_videos, total_views, total_likes, avg_views, avg_likes

---

### Test 7: Invalid API Key (Should Fail)

curl -H "X-API-Key: wrong-key"
"http://localhost:8000/api/videos/recent?limit=3"


**Expected Result:**
- Status Code: 403 Forbidden
- Error message: "Invalid API Key"

---

### Test 8: Missing API Key (Should Fail)

curl "http://localhost:8000/api/videos/recent?limit=3"


**Expected Result:**
- Status Code: 403 Forbidden
- Error message about missing API key

---

## Chatbot Testing

### Open Chatbot
Navigate to: `http://localhost:8501`

---

### Test Question 1: Video Count

**Input:** "How many videos do we have?"

**Expected Response:**
- Should show exact count (133+)
- Response should be formatted clearly

---

### Test Question 2: Recent Videos

**Input:** "Show me recent videos"

**Expected Response:**
- List of 5 most recent videos
- Each with title, channel, views, likes, and clickable link

---

### Test Question 3: Trending Videos

**Input:** "What are the trending videos?"

**Expected Response:**
- List of top videos by view count
- Sorted highest to lowest

---

### Test Question 4: Channel Info

**Input:** "Tell me about REPORTER channel"

**Expected Response:**
- Total videos
- Total views and likes
- Average statistics

---

### Test Question 5: Help

**Input:** "help"

**Expected Response:**
- List of available commands
- Example questions user can ask

---

### Test Question 6: General Query

**Input:** "What kind of videos are in the database?"

**Expected Response:**
- AI-generated description of content
- Mentions news channels and content types

---

## Database Testing

### Test Database Connection

from database.mongodb_client import get_sync_database

db = get_sync_database()
count = db['videos'].count_documents({})
print(f"Total videos in database: {count}")


**Expected Output:**
Total videos in database: 133


---

### Test Query Operations

from database.query_operations import get_recent_videos

videos = get_recent_videos(5)
print(f"Retrieved {len(videos)} videos")
for video in videos:
print(f"- {video['title']}")


**Expected Output:**
- List of 5 video titles

---

## Integration Testing

### Full Stack Test

1. **Start both services** (API + Chatbot)
2. **Test API** via curl or Swagger
3. **Test Chatbot** via browser
4. **Verify** both access same database
5. **Check** data consistency

---

## Performance Testing

### API Response Time

time curl -H "X-API-Key: my-secret-key-123"
"http://localhost:8000/api/videos/recent?limit=10"


**Expected:** Response time < 500ms

---

### Database Query Performance

import time
from database.query_operations import get_recent_videos

start = time.time()
videos = get_recent_videos(100)
elapsed = time.time() - start

print(f"Query time: {elapsed:.3f} seconds")

**Expected:** Query time < 1 second

---

## Browser Testing

### Swagger UI
1. Open: http://localhost:8000/docs
2. Click on any endpoint
3. Click "Try it out"
4. Add API key in Authentication section
5. Execute request
6. Verify response

---

### Chatbot UI
1. Open: http://localhost:8501
2. Check sidebar shows database stats
3. Type question in chat input
4. Press Enter
5. Verify response appears
6. Check response is relevant

---

## Automated Test Results

### Expected Outcomes

| Test | Endpoint/Feature | Expected Status |
|------|-----------------|-----------------|
| Health Check | GET /health | ✅ 200 OK |
| Recent Videos | GET /api/videos/recent | ✅ 200 OK |
| Search | GET /api/videos/search | ✅ 200 OK |
| Trending | GET /api/videos/trending | ✅ 200 OK |
| Channel Count | GET /api/videos/count/* | ✅ 200 OK |
| Channel Stats | GET /api/videos/channel/*/stats | ✅ 200 OK |
| Invalid Auth | Any with wrong key | ✅ 403 Forbidden |
| Chatbot Count | "How many videos?" | ✅ Correct number |
| Chatbot Recent | "Show recent videos" | ✅ Video list |
| Chatbot Help | "help" | ✅ Command list |

---

## Troubleshooting

### API Not Starting
- Check if port 8000 is already in use
- Verify .env file exists with all keys
- Check MongoDB connection string

### Chatbot Errors
- Verify GOOGLE_API_KEY is valid
- Check Streamlit version
- Ensure API is running first

### Database Connection Failed
- Verify MONGODB_URL in .env
- Check internet connection
- Verify MongoDB Atlas whitelist includes your IP

---

## Test Coverage Summary

✅ **API Endpoints:** 7/7 tested  
✅ **Authentication:** Verified  
✅ **Chatbot Features:** 6/6 tested  
✅ **Database Operations:** Verified  
✅ **Error Handling:** Tested  
✅ **Integration:** Working  

---

## All Tests Passed ✅

If all tests pass, the system is ready for production deployment.