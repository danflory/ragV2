import jwt
import datetime
import os
import logging
from typing import Optional, Dict, List
from app.config import config

logger = logging.getLogger("Gravitas_AUTH")

# Default secret for development, MUST be overridden in production
JWT_SECRET = config.JWT_SECRET_KEY
JWT_ALGORITHM = "HS256"
TOKEN_EXPIRATION_HOURS = 24

class AuthManager:
    """
    Handles JWT token generation and verification for Ghost identities.
    """
    
    @staticmethod
    def create_token(ghost_id: str, access_groups: List[str] = None, expires_in_hours: int = TOKEN_EXPIRATION_HOURS) -> str:
        """Generates a new JWT token for a ghost."""
        payload = {
            "sub": ghost_id,
            "groups": access_groups or [],
            "iat": datetime.datetime.now(datetime.timezone.utc),
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=expires_in_hours)
        }
        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    @staticmethod
    def verify_token(token: str) -> Optional[Dict]:
        """Verifies a JWT token and returns the payload."""
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.error(f"Invalid token: {e}")
            return None
        except Exception as e:
            logger.error(f"Token verification error: {e}")
            return None

# Convenience functions
def create_access_token(ghost_id: str, groups: List[str] = None) -> str:
    return AuthManager.create_token(ghost_id, groups)

def decode_access_token(token: str) -> Optional[Dict]:
    return AuthManager.verify_token(token)
