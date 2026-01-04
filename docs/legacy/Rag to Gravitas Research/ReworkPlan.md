Based on the comprehensive audit of your documentation and codebase, the plan focuses on synchronizing the "Legacy" implementation with the "v4.0 Gravitas Grounded Research" specification. Currently, a critical "Instruction Drift" exists: your specs describe a Dual-GPU, Qdrant-based system, but the actual code (app/memory.py, app/config.py) executes single-GPU ChromaDB logic.

1. Architectural Enforcement (The "Constitution")
We will immediately enforce patterns.md as the immutable source of truth. This document explicitly bans "Anti-Patterns" currently present in the code, such as storing raw text payloads in the vector database. It mandates the Gravitas Grounded Research Separation Pattern, requiring that:

Indices (Vectors) live in Qdrant (GPU 1 optimized).

Blobs (Content) live in MinIO (S3 Protocol).

State: The Titan RTX must operate via a Hardware State Machine, strictly switching between "Reflex Mode" (Gemma-2) and "Dev Mode" (DeepSeek) to prevent the OOM crashes predicted by your hardware constraints.

2. The Code Migration (The "Brain Transplant")
The development process will execute Phase 4.1, prioritizing infrastructure over features. We will ignore the broken legacy tests and build a new foundation:

Storage Layer: Create app/storage.py implementing the ObjectStore interface to handle MinIO interactions.

Memory Layer: Refactor app/memory.py to replace ChromaDB with QdrantClient, enforcing Hybrid Search (Dense + Sparse) as defined in your spec.

Wiring: Update app/container.py to inject these new dependencies, strictly adhering to the Inversion of Control (IoC) principle.

3. Process Hardening (The "Receipt" Protocol)
We will shift the Agent workflow from "Fire-and-Forget" to "Trust-but-Verify."

Input: The Coder receives todo.md (Tasks) and interfaces.py (Contracts).

Constraint: No code is written without a failing test (tests/test_minio_storage.py).

Output: The definition of "Done" changes. The Coder must submit a completed.md "Receipt" containing the raw pytest logs.

Gatekeeping: I (The Architect) will reject any Receipt that violates the patterns.md Constitution, forcing an immediate correction loop before the code is merged.

This plan turns your codebase from a "Chat App" into the robust "Research Lab" described in your vision.