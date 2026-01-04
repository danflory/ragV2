import pytest
import asyncio
import uuid
from app.storage import MinioConnector

@pytest.mark.asyncio
async def test_minio_upload_download():
    """Verify that we can upload and download data from MinIO."""
    # Note: Assumes MinIO is running on localhost:9000 with default credentials
    # In a CI environment, these would be injected via environment variables.
    connector = MinioConnector(
        endpoint="localhost:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        bucket_name="test-bucket",
        secure=False
    )
    
    test_key = f"test-{uuid.uuid4()}.txt"
    test_content = "Hello Omni-RAG! This is a test blob."
    
    # Test Upload
    upload_success = await connector.upload(test_key, test_content)
    assert upload_success is True, "Failed to upload to MinIO"
    
    # Test Retrieval
    retrieved_content = await connector.get(test_key)
    assert retrieved_content == test_content, f"Content mismatch: expected {test_content}, got {retrieved_content}"
    
    # Test non-existent key
    missing_content = await connector.get("non-existent-key-12345.txt")
    assert missing_content is None, "Expected None for non-existent key"
