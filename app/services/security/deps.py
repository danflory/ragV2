
import os
from typing import Optional, Dict
from fastapi import Header, HTTPException
from app.services.security.auth import decode_access_token

async def get_current_user(authorization: Optional[str] = Header(None)) -> Dict:
    """FastAPI dependency to retrieve the authenticated user."""
    if os.getenv("AUTH_DISABLED", "false").lower() == "true":
        return {"sub": "Supervisor_Managed_Agent", "groups": ["admin"]}
        
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    
    token = authorization.replace("Bearer ", "")
    payload = decode_access_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
        
    return payload
