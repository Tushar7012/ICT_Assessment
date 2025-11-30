# API Documentation

## Base URL
    http://localhost:8000

## Authentication

All endpoints (except `/health`) require API Key authentication.

**Header:**
    X-API-Key: your-api-key-here


---

## Endpoints

### 1. Health Check

**Endpoint:** `GET /health`  
**Authentication:** Not required  
**Description:** Check API health status

**Example Request:**
    curl http://localhost:8000/health


**Response:**
    {
    "status": "healthy",
    "database": "connected",
    "total_videos": 133,
    "api_version": "1.0.0"
    }


---

### 2. Get Recent Videos

**Endpoint:** `GET /api/videos/recent`  
**Authentication:** Required  
**Parameters:**
- `limit` (optional): Number of videos (default: 10, max: 100)

**Example Request:**
    curl -H "X-API-Key: my-secret-key-123""http://localhost:8000/api/videos/recent?limit=5"

**Response:**
    {
    "status": "success",
    "count": 5,
    "videos": [
    {
    "video_id": "abc123",
    "title": "Breaking News: Latest Update",
    "channel_title": "REPORTER LIVE",
    "view_count": 15000,
    "like_count": 500,
    "upload_date": "2025-11-30T10:30:00",
    "url": "https://youtube.com/watch?v=abc123"
    }
    ]
    }

---

### 3. Search Videos

**Endpoint:** `GET /api/videos/search`  
**Authentication:** Required  
**Parameters:**
- `keyword` (required): Search term
- `limit` (optional): Max results (default: 10, max: 50)

**Example Request:**
curl -H "X-API-Key: my-secret-key-123"
"http://localhost:8000/api/videos/search?keyword=news&limit=5"


**Response:**
{
"status": "success",
"count": 5,
"keyword": "news",
"videos": [...]
}

---

### 4. Get Trending Videos

**Endpoint:** `GET /api/videos/trending`  
**Authentication:** Required  
**Parameters:**
- `limit` (optional): Number of videos (default: 10, max: 50)

**Description:** Returns videos sorted by view count (highest first)

**Example Request:**
curl -H "X-API-Key: my-secret-key-123"
"http://localhost:8000/api/videos/trending?limit=10"


**Response:**
{
"status": "success",
"count": 10,
"videos": [...]
}

---

### 5. Count Channel Videos

**Endpoint:** `GET /api/videos/count/{channel_name}`  
**Authentication:** Required  
**Path Parameters:**
- `channel_name`: Name of the YouTube channel

**Example Request:**
curl -H "X-API-Key: my-secret-key-123"
"http://localhost:8000/api/videos/count/REPORTER"

**Response:**
{
"status": "success",
"channel": "REPORTER",
"video_count": 115
}


---

### 6. Get Channel Statistics

**Endpoint:** `GET /api/videos/channel/{channel_name}/stats`  
**Authentication:** Required  
**Path Parameters:**
- `channel_name`: Name of the YouTube channel

**Example Request:**
curl -H "X-API-Key: my-secret-key-123"
"http://localhost:8000/api/videos/channel/REPORTER/stats"


**Response:**
{
"status": "success",
"channel": "REPORTER",
"statistics": {
"total_videos": 115,
"total_views": 5000000,
"total_likes": 150000,
"avg_views": 43478,
"avg_likes": 1304
}
}

---

### 7. Get Channel Recent Videos

**Endpoint:** `GET /api/videos/channel/{channel_name}/recent`  
**Authentication:** Required  
**Path Parameters:**
- `channel_name`: Name of the YouTube channel
**Query Parameters:**
- `hours` (optional): Time range in hours (default: 24, max: 720)

**Example Request:**
curl -H "X-API-Key: my-secret-key-123"
"http://localhost:8000/api/videos/channel/REPORTER/recent?hours=24"


**Response:**
{
"status": "success",
"channel": "REPORTER",
"hours": 24,
"video_count": 5
}

---

## Error Responses

### 403 Forbidden (Invalid API Key)
{
"detail": "Invalid API Key"
}


### 404 Not Found
{
"detail": "Channel 'XYZ' not found"
}

### 422 Validation Error
{
"detail": [
{
"loc": ["query", "limit"],
"msg": "value is not a valid integer",
"type": "type_error.integer"
}
]
}

---

## Rate Limiting

Currently no rate limiting is implemented. For production, consider:
- 100 requests per minute per API key
- 1000 requests per hour per API key

---

## Interactive Documentation

**Swagger UI:** http://localhost:8000/docs  
**ReDoc:** http://localhost:8000/redoc

Both provide interactive API testing interfaces where you can:
- View all endpoints
- Test requests directly
- See response schemas
- Download OpenAPI specification

---

## Authentication Examples

### cURL
curl -H "X-API-Key: your-key-here" http://localhost:8000/api/videos/recent


### Python (requests)
import requests

headers = {'X-API-Key': 'your-key-here'}
response = requests.get('http://localhost:8000/api/videos/recent', headers=headers)
print(response.json())


### JavaScript (fetch)
fetch('http://localhost:8000/api/videos/recent', {
headers: {
'X-API-Key': 'your-key-here'
}
})
.then(response => response.json())
.then(data => console.log(data));

---

## Support

For issues or questions, please open an issue on GitHub:
https://github.com/Tushar7012/ICT_Assessment/issues