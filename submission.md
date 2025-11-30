# YouTube Metadata Pipeline - Final Submission

## Student Information
**Name:** Tushar  
**Project:** YouTube Real-Time Metadata Pipeline  
**Date:** November 30, 2025  
**Repository:** https://github.com/Tushar7012/ICT_Assessment

---

## ✅ Deliverables Completed

### 1. Database Layer
- **Technology:** MongoDB Atlas (Cloud)
- **Status:** ✅ Operational
- **Data:** 133+ YouTube videos ingested
- **Channels:** REPORTER LIVE, ANI News
- **Features:** 
  - Cloud-hosted database
  - Indexed queries
  - Real-time data access

### 2. REST API
- **Framework:** FastAPI
- **Status:** ✅ Fully Functional
- **Endpoints:** 7 endpoints
  - `GET /health` - Health check (no auth)
  - `GET /api/videos/recent` - Get recent videos
  - `GET /api/videos/search` - Search by keyword
  - `GET /api/videos/trending` - Get trending videos
  - `GET /api/videos/count/{channel}` - Count channel videos
  - `GET /api/videos/channel/{channel}/stats` - Channel statistics
  - `GET /api/videos/channel/{channel}/recent` - Recent by channel
- **Authentication:** API Key (X-API-Key header)
- **Documentation:** OpenAPI/Swagger at `/docs`

### 3. AI-Powered Chatbot
- **Framework:** Streamlit
- **AI Model:** Google Gemini Pro
- **Status:** ✅ Working
- **Features:**
  - Natural language queries
  - Real-time database access
  - Video statistics
  - Channel analytics
  - Trending analysis

### 4. Docker Deployment
- **Status:** ✅ Configured
- **Files:**
  - `Dockerfile` - Container definition
  - `docker-compose.yml` - Multi-service orchestration
  - `.dockerignore` - Build optimization
- **Services:**
  - API service (port 8000)
  - Chatbot service (port 8501)

### 5. CI/CD Pipeline
- **Platform:** GitHub Actions
- **Status:** ✅ Active
- **Workflow:** `.github/workflows/ci-cd.yml`
- **Jobs:**
  - Build and test
  - Docker validation
  - Security check
  - Deployment ready notification

### 6. Documentation
- **README.md** - Complete project documentation
- **API Documentation** - Auto-generated Swagger
- **Code Comments** - Inline documentation
- **Deployment Guide** - Setup instructions

---

## 🛠️ Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Language | Python | 3.11+ |
| API Framework | FastAPI | 0.104+ |
| Database | MongoDB Atlas | Cloud |
| Chatbot UI | Streamlit | 1.28+ |
| AI Model | Google Gemini | Pro |
| Containerization | Docker | Latest |
| CI/CD | GitHub Actions | - |
| Data Source | YouTube API | v3 |

---

## 🚀 How to Run

### Prerequisites
- Python 3.11 or higher
- MongoDB Atlas account
- YouTube Data API key
- Google Gemini API key

### Installation Steps

1. **Clone Repository**
    ```git clone https://github.com/Tushar7012/ICT_Assessment.git
    cd ICT_Assessment```

2. **Create Virtual Environment**
    python -m venv venv
    venv\Scripts\activate


3. **Install Dependencies**
    pip install -r requirements.txt

4. **Configure Environment**
    Create `.env` file with:
    YOUTUBE_API_KEY=your_youtube_api_key
    MONGODB_URL=your_mongodb_atlas_url
    API_KEY=your_custom_api_key
    GOOGLE_API_KEY=your_gemini_api_key


5. **Run API Server**
    uvicorn api.main:app --host 0.0.0.0 --port 8000


6. **Run Chatbot** (in new terminal)
    streamlit run chatbot/app.py
    
### Access Points
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Chatbot: http://localhost:8501

---

## 🧪 Testing

### API Testing

**Health Check:**
    curl http://localhost:8000/health

**Get Recent Videos:**
    curl -H "X-API-Key: my-secret-key-123" "http://localhost:8000/api/videos/recent?limit=5"

**Search Videos:**
    curl -H "X-API-Key: my-secret-key-123" "http://localhost:8000/api/videos/search?keyword=news&limit=5"


### Chatbot Testing
1. Open http://localhost:8501
2. Ask: "How many videos do we have?"
3. Ask: "Show me recent videos"
4. Ask: "What are trending videos?"

---

## 🐳 Docker Deployment

### Build and Run
    docker-compose up -d


### Stop Services
    docker-compose down


---

## 📊 Project Statistics

- **Total Code Files:** 15+
- **Lines of Code:** 1500+
- **API Endpoints:** 7
- **Database Records:** 133+ videos
- **Test Coverage:** Manual testing completed
- **Documentation Pages:** Multiple

---

## ✨ Key Features Implemented

1. **Cloud-Native Architecture**
   - MongoDB Atlas cloud database
   - Stateless API design
   - Container-ready deployment

2. **Enterprise-Grade API**
   - RESTful design
   - API key authentication
   - Comprehensive error handling
   - Auto-generated documentation

3. **AI Integration**
   - Google Gemini Pro integration
   - Natural language processing
   - Context-aware responses

4. **DevOps Best Practices**
   - Docker containerization
   - CI/CD pipeline
   - Automated testing
   - Code quality checks

5. **Scalability**
   - Microservices architecture
   - Horizontal scaling ready
   - Database indexing

---

## 🔒 Security Features

- API key authentication
- Environment variable configuration
- No hardcoded credentials
- .gitignore for sensitive files
- MongoDB Atlas security

---

## 📈 Future Enhancements

- Real-time data ingestion with webhooks
- User authentication and authorization
- Advanced analytics dashboard
- Video recommendation engine
- Rate limiting and caching
- Kubernetes deployment

---

## 📞 Contact

**GitHub:** https://github.com/Tushar7012/ICT_Assessment  
**Repository Issues:** https://github.com/Tushar7012/ICT_Assessment/issues

---

## ✅ Submission Checklist

- [x] MongoDB database with 133+ videos
- [x] REST API with 7 endpoints
- [x] API authentication implemented
- [x] AI chatbot with Gemini integration
- [x] Docker configuration complete
- [x] GitHub Actions CI/CD pipeline
- [x] Comprehensive README.md
- [x] Code properly commented
- [x] Environment configuration documented
- [x] Testing instructions provided
- [x] All code pushed to GitHub
- [x] Repository is public

---

**All requirements successfully completed and ready for evaluation!**

