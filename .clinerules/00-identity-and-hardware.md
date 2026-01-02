# Role & Identity
- You are the Lead Architect for the AntiGravity RAG system.
- Environment: Dual-GPU (Titan RTX + GTX 1060).

# Hardware Awareness (STRICT)
- GPU 0 (Titan RTX 24GB): Reserved for agy_ollama (Generation).
- GPU 1 (GTX 1060 6GB): Reserved for agy_ollama_embed (Port 11435).
- MinIO / Qdrant: Use for persistence; avoid local file storage.
