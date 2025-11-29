from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY", "your-secret-api-key")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def verify_api_key(api_key: str = Security(api_key_header)):
    """Verify API key authentication (Bonus Feature)"""
    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="Missing API Key. Include 'X-API-Key' header."
        )
    if api_key != API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Invalid API Key"
        )
    return api_key
    