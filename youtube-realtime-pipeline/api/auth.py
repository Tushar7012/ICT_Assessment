import os
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment
API_KEY = os.getenv("API_KEY", "my-secret-key-123")

# Print for debugging
print(f"\n{'='*60}")
print(f"🔑 LOADED API KEY: '{API_KEY}'")
print(f"{'='*60}\n")

# Define API key header
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

def verify_api_key(api_key: str = Security(api_key_header)):
    """
    Verify API key from request header
    
    Args:
        api_key: API key from X-API-Key header
        
    Returns:
        str: Validated API key
        
    Raises:
        HTTPException: If API key is invalid
    """
    if api_key != API_KEY:
        raise HTTPException(
            status_code=403, 
            detail="Invalid API Key"
        )
    return api_key
