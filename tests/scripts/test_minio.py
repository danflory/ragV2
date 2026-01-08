#!/usr/bin/env python3
"""
Test script to verify MinIO connection and bucket creation.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.config import config
from minio import Minio

def test_minio_connection():
    """Test MinIO connection and bucket creation."""
    print("Testing MinIO connection...")
    
    try:
        # Create MinIO client
        client = Minio(
            config.MINIO_ENDPOINT,
            access_key=config.MINIO_ACCESS_KEY,
            secret_key=config.MINIO_SECRET_KEY,
            secure=config.MINIO_SECURE
        )
        # Enable path-style access for MinIO version 7.2.20
        client._use_path_style = True
        
        print(f"Connected to MinIO at {config.MINIO_ENDPOINT}")
        
        # Check if bucket exists
        bucket_exists = client.bucket_exists(config.MINIO_BUCKET)
        print(f"Bucket '{config.MINIO_BUCKET}' exists: {bucket_exists}")
        
        # Create bucket if it doesn't exist
        if not bucket_exists:
            print(f"Creating bucket '{config.MINIO_BUCKET}'...")
            client.make_bucket(config.MINIO_BUCKET)
            print("Bucket created successfully!")
        else:
            print("Bucket already exists.")
            
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    success = test_minio_connection()
    sys.exit(0 if success else 1)
