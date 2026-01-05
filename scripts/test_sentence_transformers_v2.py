import sys
# Force output to unbuffered
sys.stdout.reconfigure(line_buffering=True)

from sentence_transformers import SentenceTransformer
import time

print("Loading model...", flush=True)
try:
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("Model loaded successfully", flush=True)
    
    sentences = ["This is a test sentence"]
    embeddings = model.encode(sentences)
    print(f"Encoded shape: {embeddings.shape}", flush=True)
except Exception as e:
    print(f"Error: {e}", flush=True)
