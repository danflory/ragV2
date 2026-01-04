### 3. STRATEGIC ROADMAP (The Docker Evolution)

#### PHASE 1: THE MEMORY (COMPLETED)
* [x] **Infrastructure:** Provision `chroma_db` container.
* [x] **Connection:** Verify Network Link (Brain -> Memory).
* [x] **Software:** Implement `VectorStore` class.
* [x] **Verification:** Pass `tests/test_memory_logic.py`.
* [x] **Feature:** "Ingest" - Build the document reader (`app/ingest.py`).

#### PHASE 2: THE AMNESIA FIX (COMPLETED)
* [x] **Goal:** Eliminate file-based SQLite state.
* [x] **Infra:** Provision `postgres_db` container.
* [x] **Software:** Implement `app/database.py` (Async PG Driver).
* [x] **Verification:** History survives container restart.

#### PHASE 3: THE BRAIN TRANSPLANT (COMPLETED)
* **Goal:** Eliminate host-dependency on Ollama.
* **Action:** Move L1 (Ollama) into a Docker service with GPU passthrough.
* **Why:** True portability. The project becomes "Run anywhere."

#### BACKLOG / TECH DEBT
* **Protocol Mismatch:** [RESOLVED] All layers now use `<reflex action="git_sync">`.
* **Secret Hygiene:** Scan codebase for hardcoded keys before pushing to public repo.