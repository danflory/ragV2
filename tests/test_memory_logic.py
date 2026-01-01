import os
import sys
import asyncio
import chromadb
from datetime import datetime

# Add the project root to sys.path so we can import 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.memory import VectorStore, save_interaction, retrieve_short_term_memory
from app.database import db

async def test_memory_logic():
    print("🧪 PROBE: Testing Hybrid Memory System...")
    
    # 0. INITIALIZE DB
    await db.connect()
    if not db.is_ready():
        print("   ❌ DATABASE: Failed to initialize connection pool.")
        return
    
    # 1. TEST VECTOR STORE (Chroma)
    print("\n[1] Testing Vector Store (Long-term)...")
    try:
        store = VectorStore()
        
        test_text = "AntiGravity uses a hybrid memory architecture."
        test_id = f"test_hybrid_{datetime.now().strftime('%M%S')}"
        
        store.add_texts(
            texts=[test_text],
            metadatas=[{"source": "test_script"}],
            ids=[test_id]
        )
        
        results = store.search("hybrid memory", n_results=1)
        if results and "hybrid memory architecture" in results[0]:
            print("   ✅ VECTOR: Stored & Retrieved successfully.")
        else:
            print(f"   ❌ VECTOR FAILED. Got: {results}")
    except Exception as e:
         print(f"   ❌ VECTOR CRASH: {e}")

    # 2. TEST POSTGRES (Short-term)
    print("\n[2] Testing Postgres (Short-term)...")
    try:
        await save_interaction("user", "Hello Memory!")
        await save_interaction("assistant", "Hello Human!")
        
        history = await retrieve_short_term_memory()
        if "USER: Hello Memory!" in history and "ASSISTANT: Hello Human!" in history:
                print("   ✅ POSTGRES: History saved & retrieved.")
        else:
                print(f"   ❌ POSTGRES FAILED. Got:\n{history}")
    except Exception as e:
        print(f"   ❌ POSTGRES CRASH: {e}")

    # 3. SHUTDOWN
    await db.disconnect()
    
    print("\n🎉 MEMORY SYSTEMS VERIFIED.")

if __name__ == "__main__":
    asyncio.run(test_memory_logic())