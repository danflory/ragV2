import io
import asyncio
import logging
from typing import Optional
from minio import Minio
from minio.error import S3Error
from app.interfaces import ObjectStore

logger = logging.getLogger("Gravitas_STORAGE")

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
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
        except S3Error as e:
            logger.critical(f"MinIO S3Error during init: {e}")
        except Exception as e:
            logger.critical(f"MinIO connection failed during init: {e}")

    async def check_health(self) -> bool:
        """Verifies connectivity to MinIO."""
        try:
            return await asyncio.to_thread(self.client.bucket_exists, self.bucket_name)
        except Exception:
            return False

    async def purge(self) -> bool:
        """
        Wipes all objects in the bucket.
        """
        try:
            # Wrap synchronous MinIO calls in to_thread
            objects = await asyncio.to_thread(self.client.list_objects, self.bucket_name, recursive=True)
            for obj in objects:
                await asyncio.to_thread(self.client.remove_object, self.bucket_name, obj.object_name)
            logger.info(f"🧹 STORAGE PURGED: All blobs removed from {self.bucket_name}")
            return True
        except S3Error as e:
            logger.error(f"❌ MINIO API ERROR (Purge): {e}")
            return False
        except Exception as e:
            logger.error(f"❌ STORAGE SYSTEM ERROR (Purge): {e}")
            return False

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
        except S3Error as e:
             logger.error(f"❌ MINIO API ERROR (Upload): {e}")
             return False
        except Exception as e:
            logger.error(f"❌ STORAGE SYSTEM ERROR (Upload): {e}")
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
        except S3Error:
             # Regular "Not Found" or similar, just return None for the getter logic
             logger.warning(f"MinIO: Object {key} not found or inaccessible.")
             return None
        except Exception as e:
            logger.error(f"❌ STORAGE SYSTEM ERROR (Get): {e}")
            return None
