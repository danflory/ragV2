from sentence_transformers import SentenceTransformer
import time

print("Loading model...")
start = time.time()
model = SentenceTransformer('all-MiniLM-L6-v2')
print(f"Loaded in {time.time() - start:.2f}s")

sentences = ["This is a test sentence", "Each sentence is converted"]
print("Encoding...")
start = time.time()
embeddings = model.encode(sentences)
print(f"Encoded in {time.time() - start:.2f}s")
print(f"Shape: {embeddings.shape}")
