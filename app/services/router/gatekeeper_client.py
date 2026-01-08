import httpx
import os
import logging
from typing import Optional, Dict

logger = logging.getLogger("Gravitas_ROUTER_GATEKEEPER_CLIENT")

GATEKEEPER_URL = os.getenv("GATEKEEPER_URL", "http://gravitas_gatekeeper:8001")

class GatekeeperClient:
    """
    Client for interacting with the Gatekeeper Microservice.
    No local fallback in Router service (Architecture decoupling).
    """
    def __init__(self):
        self.url = GATEKEEPER_URL
        
    async def validate_request(self, token: str, action: str, resource: str, metadata: Dict = None) -> Dict:
        """
        Validates a request via Gatekeeper.
        """
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                payload = {
                    "action": action,
                    "resource": resource,
                    "metadata": metadata
                }
                headers = {"Authorization": f"Bearer {token}"}
                
                response = await client.post(f"{self.url}/validate", json=payload, headers=headers)
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code in [401, 403]:
                    return {"allowed": False, "error_code": response.status_code, "detail": response.json().get("detail")}
                else:
                    logger.warning(f"Gatekeeper returned unexpected status {response.status_code}")
                    return {"allowed": False, "error_code": 503, "detail": "Gatekeeper error"}
                    
        except httpx.RequestError as e:
            logger.error(f"Gatekeeper unreachable: {e}")
            return {"allowed": False, "error_code": 503, "detail": "Gatekeeper unavailable"}
        except Exception as e:
            logger.error(f"Gatekeeper client error: {e}")
            return {"allowed": False, "error_code": 500, "detail": "Internal auth error"}

gatekeeper_client = GatekeeperClient()
