from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
from api.middleware import log_requests

app = FastAPI(
    title="YouTube Metadata API",
    description="Enterprise-grade YouTube video analytics API with AI-powered insights",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "Tushar",
        "url": "https://github.com/Tushar7012/ICT_Assessment"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    }
)

# Add middleware for request logging
app.middleware("http")(log_requests)

# CORS middleware - allow all origins for demo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes (all endpoints with authentication)
app.include_router(router)

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - API information"""
    return {
        "message": "YouTube Metadata API - Enterprise Edition",
        "version": "1.0.0",
        "status": "operational",
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        },
        "endpoints": {
            "health": "/health",
            "recent_videos": "/api/videos/recent",
            "search": "/api/videos/search",
            "trending": "/api/videos/trending",
            "channel_stats": "/api/videos/channel/{channel_name}/stats"
        },
        "authentication": "API Key required in header: X-API-Key",
        "github": "https://github.com/Tushar7012/ICT_Assessment"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint - No authentication required"""
    from database.mongodb_client import get_sync_database
    try:
        db = get_sync_database()
        video_count = db['videos'].count_documents({})
        
        # Test database connection
        db.command('ping')
        
        return {
            "status": "healthy",
            "database": "connected",
            "total_videos": video_count,
            "api_version": "1.0.0",
            "services": {
                "mongodb": "operational",
                "api": "operational"
            }
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "api_version": "1.0.0"
        }

# Optional: Add startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Execute on application startup"""
    print("🚀 YouTube Metadata API is starting up...")
    print("📊 Connecting to MongoDB Atlas...")
    try:
        from database.mongodb_client import get_sync_database
        db = get_sync_database()
        video_count = db['videos'].count_documents({})
        print(f"✅ Database connected! Total videos: {video_count}")
    except Exception as e:
        print(f"⚠️  Database connection warning: {e}")
    print("✨ API is ready to accept requests!")

@app.on_event("shutdown")
async def shutdown_event():
    """Execute on application shutdown"""
    print("🛑 YouTube Metadata API is shutting down...")
    print("👋 Goodbye!")
