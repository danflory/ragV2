import io
import asyncio
import logging
from typing import Optional
from minio import Minio
from app.interfaces import ObjectStore

logger = logging.getLogger("AGY_STORAGE")

class MinioConnector(ObjectStore):
    """Implementation of ObjectStore using MinIO."""
    
    def __init__(self, endpoint: str, access_key: str, secret_key: str, bucket_name: str, secure: bool = False):
        import socket
        try:
            # Minio-py 7.x forces virtual-host style for non-IP endpoints.
            # We resolve the hostname to an IP to force path-style access.
            host_part = endpoint.split(':')[0]
            port_part = endpoint.split(':')[1] if ':' in endpoint else ('443' if secure else '80')
            ip = socket.gethostbyname(host_part)
            resolved_endpoint = f"{ip}:{port_part}"
            logger.info(f"Resolved MinIO endpoint {endpoint} -> {resolved_endpoint}")
            endpoint = resolved_endpoint
        except Exception as e:
            logger.warning(f"Could not resolve MinIO endpoint {endpoint}: {e}")

        self.client = Minio(
            endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )
        self.bucket_name = bucket_name
        self._ensure_bucket()

    def _ensure_bucket(self):
        """Ensures the bucket exists (synchronous, called in init)."""
        if not self.client.bucket_exists(self.bucket_name):
            self.client.make_bucket(self.bucket_name)

    async def upload(self, key: str, data: str) -> bool:
        """Uploads raw text content to MinIO."""
        try:
            content_bytes = data.encode("utf-8")
            # Using asyncio.to_thread to keep the sync Minio client from blocking the loop
            await asyncio.to_thread(
                self.client.put_object,
                self.bucket_name,
                key,
                io.BytesIO(content_bytes),
                length=len(content_bytes),
                content_type="text/plain"
            )
            return True
        except Exception as e:
            logger.error(f"MinIO Upload Error: {e}")
            return False

    async def get(self, key: str) -> Optional[str]:
        """Retrieves raw text content from MinIO."""
        try:
            response = await asyncio.to_thread(
                self.client.get_object,
                self.bucket_name,
                key
            )
            try:
                content = response.read().decode("utf-8")
                return content
            finally:
                response.close()
                response.release_conn()
        except Exception as e:
            logger.error(f"MinIO Get Error: {e}")
            return None
