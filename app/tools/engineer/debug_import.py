import sys
import os

# 1. Force current directory into python path (mimic pytest)
sys.path.insert(0, os.getcwd())

print("🕵️  DEBUG: Attempting to import app.router...")

try:
    # 2. Try to import the module
    import app.router
    print(f"✅ Module 'app.router' loaded from: {app.router.__file__}")
    
    # 3. Inspect what is actually inside it
    print("--------------------------------------------------")
    print(f"👀 Contents of dir(app.router):")
    attributes = dir(app.router)
    print([a for a in attributes if not a.startswith("__")])
    print("--------------------------------------------------")

    # 4. Try to access the specific function
    if 'chat_endpoint' in attributes:
        print("✅ SUCCESS: 'chat_endpoint' is present.")
    else:
        print("❌ FAILURE: 'chat_endpoint' is MISSING.")
        
except ImportError as e:
    print(f"❌ CRITICAL IMPORT ERROR: {e}")
except Exception as e:
    print(f"❌ UNEXPECTED ERROR: {e}")