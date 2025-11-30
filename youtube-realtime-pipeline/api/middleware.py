from fastapi import Request
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def log_requests(request: Request, call_next):
    """Log all API requests with timing"""
    start_time = time.time()
    
    # Process request
    response = await call_next(request)
    
    # Calculate duration
    duration = time.time() - start_time
    
    # Log request details
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Duration: {duration:.2f}s"
    )
    
    # Add custom header
    response.headers["X-Process-Time"] = str(duration)
    
    return response
