print("Minimal test start")
import os
print(f"CWD: {os.getcwd()}")
try:
    import app
    print("app imported")
except Exception as e:
    print(f"Failed to import app: {e}")
