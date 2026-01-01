# 004_HARDWARE_OPERATIONS.md
# STATUS: ACTIVE
# HARDWARE: NVIDIA Titan RTX (24GB VRAM)

## 1. INFRASTRUCTURE BINDINGS
*   **Host:** Windows 10 Pro / WSL2 (Ubuntu).
*   **GPU Passthrough:** NVIDIA Container Toolkit must be active to allow Docker containers to access the Titan RTX.
*   **Memory Allocation:** 
    *   **WSL2 Hard Limit:** 32GB RAM.
    *   **GPU Safety Pool:** Hard block at 20GB VRAM to prevent system jitter.

## 2. VRAM GUARD PROTOCOL (The "Floor")
To prevent system crashes or OOM (Out Of Memory) during long context sessions:
1.  **Strict Buffer:** 4GB (4096MB) must remain free at all times.
2.  **Logic:** Prior to any L1 inference, `GPUtil` queries the Titan RTX.
3.  **Action:** If `Free_VRAM < 4GB`, the request **must** be promoted to L2 to avoid crash.

## 3. DOCKER TOPOLOGY
The system runs in a multi-container environment:
*   **`brain`:** FastAPI application (CPU/GPU).
*   **`memory`:** ChromaDB vector store (CPU).
*   **`ollama`:** L1 model hosting (GPU Priority).
