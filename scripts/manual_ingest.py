#!/usr/bin/env python3
"""
Manual ingestion script for Gravitas RAG system.
Clears and reingests all documentation.
"""
import asyncio
import os
import sys

# Set environment for Docker network
os.environ["QDRANT_HOST"] = "Gravitas_qdrant"
os.environ["MINIO_ENDPOINT"] = "Gravitas_minio:9000"
os.environ["DB_HOST"] = "Gravitas_postgres"
os.environ["L1_URL"] = "http://Gravitas_ollama:11434"

async def main():
    print("=" * 80)
    print("GRAVITAS RAG INGESTION SCRIPT")
    print("=" * 80)
    
    try:
        from app.container import container
        print("✅ Container initialized")
        
        if not container.memory:
            print("❌ Memory not initialized")
            return 1
            
        if not container.ingestor:
            print("❌ Ingestor not initialized")
            return 1
        
        print(f"📁 Docs path: {container.ingestor.docs_path}")
        
        # 1. Purge existing memory
        print("\n🧹 Step 1: Purging existing memory...")
        purge_success = await container.memory.purge()
        if purge_success:
            print("✅ Memory purged successfully")
        else:
            print("⚠️ Memory purge may have failed")
        
        # 2. Run ingestion
        print("\n📥 Step 2: Ingesting all documents...")
        summary = await container.ingestor.ingest_all()
        
        # 3. Display results
        print("\n" + "=" * 80)
        print("INGESTION SUMMARY")
        print("=" * 80)
        print(f"Status: {summary.get('status', 'unknown')}")
        print(f"Files processed: {summary.get('files_processed', 0)}")
        print(f"Chunks ingested: {summary.get('chunks_ingested', 0)}")
        
        if summary.get('errors'):
            print(f"\n⚠️ Errors encountered: {len(summary['errors'])}")
            for error in summary['errors'][:5]:  # Show first 5 errors
                print(f"  - {error}")
        
        # 4. Verify ingestion
        print("\n🔍 Step 3: Verifying ingestion...")
        test_results = await container.memory.search("roadmap infrastructure", top_k=3)
        print(f"✅ Search test returned {len(test_results)} results")
        
        if test_results:
            print("\nFirst result preview:")
            print("-" * 80)
            print(test_results[0][:300] + "...")
            print("-" * 80)
        
        print("\n✅ INGESTION COMPLETE")
        return 0
        
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
