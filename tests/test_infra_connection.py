import sys
import os
import time

# 1. PATH HACK
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    import chromadb
    from app.config import config
except ImportError as e:
    print(f"❌ IMPORT ERROR: {e}")
    print("   (Did you run this inside the container? The local venv might not have chromadb yet.)")
    sys.exit(1)

def test_connection():
    print("🧪 PROBE: Testing Brain -> Memory Uplink...")
    print(f"   Target: {config.CHROMA_URL}")
    
    # URL parsing hack for the test (The library wants host/port split)
    # Assumes http://chroma_db:8000
    host = "chroma_db"
    port = 8000
    
    try:
        # ATTEMPT CONNECTION
        client = chromadb.HttpClient(host=host, port=port)
        
        # PING
        start = time.time()
        heartbeat = client.heartbeat()
        latency = (time.time() - start) * 1000
        
        print(f"   ✅ HEARTBEAT: {heartbeat}")
        print(f"   ⚡ LATENCY: {latency:.2f}ms")
        print("🎉 SUCCESS: The containers are linked.")
        
    except Exception as e:
        print(f"❌ CONNECTION FAILED: {str(e)}")
        print("   (Check if 'chroma_db' service is healthy in docker-compose ps)")
        sys.exit(1)

if __name__ == "__main__":
    test_connection()