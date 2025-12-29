import requests
import sys
import os

def ask_agy_to_write(prompt, filename):
    # Your verified endpoint
    url = "http://localhost:5050/ask" 
    
    print(f"🚀 Sending request to L1...")
    
    # We use GET because your main.py uses @app.get("/ask")
    # We use 'q' because your function is def ask(q: str):
    try:
        response = requests.get(url, params={"q": f"Write only code. No talk. {prompt}"}, timeout=300)
        
        if response.status_code == 200:
            data = response.json()
            # Based on your main.py: return {"answer": result} 
            # and result is {"answer": "...", "source": "..."}
            code = data['answer']['answer']
            
            # Clean up Markdown junk
            clean_code = code.replace("```python", "").replace("```", "").strip()
            
            with open(filename, "w") as f:
                f.write(clean_code)
            
            print(f"✅ Agy successfully wrote to {filename}")
            # Try to open it
            os.system(f"agy {filename}")
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python scripts/agy_writer.py 'prompt' 'filename.py'")
    else:
        ask_agy_to_write(sys.argv[1], sys.argv[2])