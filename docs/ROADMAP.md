### 3. STRATEGIC ROADMAP (The Docker Evolution)

#### PHASE 1: THE MEMORY (Current Focus)
* [x] **Infrastructure:** Provision `chroma_db` container.
* [x] **Connection:** Verify Network Link (Brain -> Memory).
* [ ] **Software:** Implement `VectorStore` class (In Progress - Waiting on Build).
* [ ] **Verification:** Pass `tests/test_memory_logic.py`.
* [ ] **Feature:** "Ingest" - Build the document reader (`app/ingest.py`).

#### PHASE 2: THE AMNESIA FIX (Next Session)
* **Goal:** Eliminate file-based SQLite state.
* **Action:** Replace `chat_history.db` with a `postgres` container.
* **Why:** Concurrency support and data safety. If the container dies, the conversation survives.

#### PHASE 3: THE BRAIN TRANSPLANT (Future)
* **Goal:** Eliminate host-dependency on Ollama.
* **Action:** Move L1 (Ollama) into a Docker service with GPU passthrough.
* **Why:** True portability. The project becomes "Run anywhere," not "Run on Dan's specific Windows setup."

#### BACKLOG / TECH DEBT
* **Protocol Mismatch:** Refactor L1 to use `<reflex action="git_sync">` instead of `<<GIT_SYNC>>`.
* **Secret Hygiene:** Scan codebase for hardcoded keys before pushing to public repo.