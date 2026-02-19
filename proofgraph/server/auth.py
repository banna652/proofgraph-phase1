import os
from fastapi import Header, HTTPException

def verify_token(authorization: str = Header(...)):
    expected = os.getenv("INGESTION_TOKEN", "devtoken")
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth header")
    
    token = authorization.split(" ", 1)[1].strip()
    if token != expected:
        raise HTTPException(status_code=403, detail="Invalid token")