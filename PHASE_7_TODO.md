# PHASE 7: THEOLOGY ENGINE (KNOWLEDGE GRAPH)

**Objective**: Upgrade Gravitas from a simple RAG system to a **Knowledge Engine** capable of ingesting, linking, and retrieving deep theological concepts from a library of ~2,000 books.

**Core Architecture**:
*   **Storage**: Neo4j (Graph) + Qdrant (Vector) + MinIO (Blob)
*   **Agent**: `GravitasLibrarian` (The Keeper of the Graph)
*   **Pipeline**: `Ingestion` -> `EntityExtraction` -> `GraphLinking`

---

## 1. Infrastructure Setup
- [ ] **Dockerize Neo4j**: Add Neo4j community edition to `docker-compose.yml`.
    - [ ] Configure persistent volumes (`data/neo4j_data`).
    - [ ] Set up secure credentials (env vars).
    - [ ] Enable APOC plugin (Awesome Procedures on Cypher) for utility functions.
- [ ] **Python Driver**: Install `neo4j` driver in `pyproject.toml` / `requirements.txt`.
- [ ] **Graph Client**: Create `app/services/graph/client.py` wrapper (Singleton pattern).
    - [ ] Implement robust connection handling and retry logic.
    - [ ] Create `wipe_graph()` method for system resets.

## 2. The Ingestion Pipeline (ETL)
- [ ] **Book Processor**: Create `app/services/ingestion/book_processor.py`.
    - [ ] Support PDF/EPUB/TXT ingestion.
    - [ ] Chunking strategy: Semantic chunking (by paragraph/topic) vs fixed size.
- [ ] **Entity Extraction**: Create `app/services/ingestion/extractor.py`.
    - [ ] Define the **Theology Schema** (Nodes: `Concept`, `Book`, `Author`, `Scripture` | Edges: `DISCUSSES`, `CITES`, `REFUTES`).
    - [ ] Prompt Engineering: Design the L3 prompt that extracts these entities from raw text.
    - [ ] Output Parsing: Ensure strict JSON output from the LLM.

## 3. The Librarian Agent (`GravitasLibrarian`)
- [ ] **Wrapper Implementation**: Create `app/wrappers/librarian_wrapper.py` (inherits from `GravitasAgentWrapper`).
- [ ] **Certification**: Create test case and pass `WrapperCertifier`.
- [ ] **Tool Access**: Give Librarian access to:
    - [ ] `read_graph(cypher_query)`
    - [ ] `write_to_graph(nodes, edges)`
    - [ ] `search_vectors(qdrant_query)`

## 4. GraphRAG (Retrieval)
- [ ] **Hybrid Searcher**: Create `app/services/search/graph_rag.py`.
    - [ ] Step 1: Vector Search (Find relevant chunks).
    - [ ] Step 2: Graph Traversal (Find related concepts 2 hops away).
    - [ ] Step 3: Synthesis (Combine into context for Theologian).
- [ ] **Supervisor Integration**: Update `Dispatcher` to route "deep" queries to GraphRAG.

## 5. Verification & Testing
- [ ] **Unit Tests**: Test Neo4j client connectivity and CRUD operations.
- [ ] **Integration Tests**:
    - [ ] Ingest 1 sample book.
    - [ ] Verify Nodes and Edges exist in Neo4j.
    - [ ] Verify Librarian can query the graph.
- [ ] **Performance Test**: Ingest 50 books and measure graph query latency.

## 6. Documentation
- [ ] **Schema Definition**: Document the official Graph Schema in `docs/009_knowledge_graph.md`.
- [ ] **Operator's Guide**: How to add books to the library.
