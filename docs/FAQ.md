# Gravitas Frequently Asked Questions (FAQ)

## Core Concepts

### What is Gravitas?
**Gravitas Grounded Research** is a high-performance, agentic RAG (Retrieval-Augmented Generation) platform designed for "zero-hallucination" engineering and deep document synthesis. Unlike traditional AI assistants, Gravitas is **Grounded**: every response is backed by a verifiable research trail in the vector store and object storage.

Gravitas is a **Dual-GPU Production-Grade Hybrid RAG Architecture** that integrates local codebases, remote documentation, and unstructured data into a unified memory system called **Omni-RAG**.

**Key Features:**
- **3-Layer Cognitive Brain:** L1 (Reflex/Local), L2 (Reasoning/Cloud), L3 (Research/Elite)
- **Dual-GPU Architecture:** Titan RTX (24GB) for generation, GTX 1060 (6GB) for embeddings
- **Hybrid Memory:** Qdrant vector database + MinIO object storage
- **Governance:** Strict 3-layer hierarchy with Gatekeeper security
- **TDD-First:** Test-driven development with comprehensive test suites

### What is Gravitas used for?
Gravitas is designed for:
1. **Zero-hallucination engineering:** All responses grounded in verified documentation
2. **Deep research and synthesis:** Combining multiple sources into coherent insights
3. **Agentic software development:** Autonomous code generation with full context awareness
4. **Knowledge base Q&A:** Answering technical questions from internal documentation
5. **Code understanding:** Analyzing and explaining complex codebases

### What is the difference between Gravitas and Antigravity?
- **Gravitas:** The production RAG system and its internal AI workers (Librarian, Scout, etc.)
- **Antigravity:** The external AI assistant (like me) that builds and manages the Gravitas project

Think of it this way: Antigravity is the developer/architect, Gravitas is the product being developed.

## Architecture

### What is the 3-layer brain?
The 3-layer brain is Gravitas's intelligent routing system that optimizes inference costs:

1. **L1 (Reflex/Local):** Fast, local inference using Ollama on the Titan RTX. Handles 80%+ of queries.
2. **L2 (Reasoning/Cloud):** Mid-tier cloud models (DeepInfra) for complex reasoning.
3. **L3 (Research/Elite):** High-end models (Gemini 3 Pro) for deep research and architectural decisions.

Queries automatically escalate if L1 can't handle them, maximizing performance while minimizing costs.

### How does the dual-GPU setup work?
Gravitas uses two NVIDIA GPUs in parallel:

- **GPU 0 (Titan RTX 24GB):** The "Brain Engine" - dedicated to LLM inference and text generation
- **GPU 1 (GTX 1060 6GB):** The "Memory Engine" - dedicated to embedding generation and vector operations

This separation prevents resource contention and allows parallel processing of generation and retrieval tasks.

### What is Qdrant?
Qdrant is the vector database used by Gravitas to store and search document embeddings. It supports:
- **Dense vector search:** Semantic similarity using neural embeddings
- **Sparse vector search:** Keyword-based BM25 matching  
- **Hybrid search:** Combining dense and sparse for best results

Gravitas uses Qdrant's hybrid search to find the most relevant documentation chunks for each query.

### What is MinIO?
MinIO is the object storage system used by Gravitas to store raw document content. While Qdrant stores vector embeddings for search, MinIO stores the full text of documents for retrieval and display.

**Architecture:**
- **Qdrant:** Semantic search → Find relevant document IDs
- **MinIO:** Blob storage → Retrieve full content by ID

## Development

### Does Gravitas follow TDD (Test-Driven Development)?
Yes! TDD is "the law of the land" for Gravitas. Every feature requires:
1. **Red:** Write a failing test first
2. **Green:** Write code to make the test pass
3. **Refactor:** Optimize while keeping tests passing

The project has comprehensive test coverage in `tests/` including:
- API endpoint tests
- RAG retrieval tests
- GPU allocation tests
- Security/Gatekeeper tests
- Integration tests

### How do I run the test suite?
```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_hybrid_search.py -v

# Run with coverage report
pytest tests/ --cov=app --cov-report=html
```

### What is the Journal Rule?
All architectural decisions and reasoning must be documented in the project journals. This ensures:
- **Forensic accountability:** Every decision has a paper trail
- **Knowledge continuity:** New developers can understand past choices
- **Self-improvement:** The AI can learn from past decisions

Journals are in `docs/journals/` and are gitignored for privacy.

### What is the Receipt Rule?
No task is considered complete until a verification receipt is generated. This ensures:
- TDD compliance (all tests pass)
- Forensic accountability (record of what was done)
- Quality assurance (changes were verified)

## Features

### What is the Nexus Dashboard?
The Nexus Dashboard is the primary web UI for Gravitas, accessible at `http://localhost:5050`. Features include:
- **Real-time chat** with LLM layers
- **Mode switching** between RAG Mode (Research) and DEV Mode (Refactoring)
- **Financial HUD** tracking inference costs and ROI
- **Agent control** for deploying Librarian and Scout agents
- **Health monitoring** with live GPU and container stats

### What is RAG mode vs DEV mode?
- **RAG Mode:** Research-focused. Queries search the knowledge base for grounded answers.
- **DEV Mode:** Development-focused. Queries can trigger reflex actions (shell commands, file writes, git operations).

These modes are mutually exclusive for security reasons.

### What is the Gatekeeper?
The Gatekeeper (`app/safety.py`) is Gravitas's security layer that:
- Validates all commands before execution
- Blocks dangerous operations (rm -rf, sudo, etc.)
- Escalates risky commands to higher layers (L2/L3) for review
- Maintains an audit log of all actions

All reflex actions (shell, write, git) pass through the Gatekeeper.

## System Management

### How do I check system health?
```bash
# Check GPU status
nvidia-smi

# Check Docker containers
docker-compose ps

# Run health monitor
./scripts/monitor.sh

# Check API health endpoint
curl http://localhost:5050/health
```

### How do I reset the Gravitas system?
If the system enters a "Split Brain" state or services fail:

```bash
# Total system reset
./scripts/reset_gravitas.sh

# Or manual reset
docker-compose down
docker-compose up -d
```

### What ports does Gravitas use?
- **5050:** Main API and Nexus Dashboard
- **11434:** Ollama (GPU 0 - Generation)
- **11435:** Ollama Embed (GPU 1 - Embeddings)
- **6333-6334:** Qdrant vector database
- **9000-9001:** MinIO object storage
- **5432:** PostgreSQL chat history

## Roadmap

### What version is Gravitas currently?
**Version 4.2.0** - "Gravitas Rebrand & Agentic Construction"

The system is in active development with a stable core infrastructure.

### What are the upcoming features?
Key planned features (see `ROADMAP.md` for details):
- **Phase 4.5:** Granular telemetry calibration with sub-second metrics
- **Phase 5:** Dynamic model governance based on performance data
- **Phase 6:** Self-learning via Reasoning Pipes
- **Phase 7:** Advanced knowledge indexing with hierarchical summarization
- **Phase 8:** Agent specialization (YouTube transcription, web scraping)
- **Phase 9:** Agentic infrastructure (.gravitas_agent directories)
- **Phase 10:** Automated model benchmarking

### Is Gravitas production-ready?
**Yes, for most use cases.** The core infrastructure is stable:
- ✅ Dockerized deployment
- ✅ Dual-GPU orchestration
- ✅ Hybrid RAG pipeline (Qdrant + MinIO)
- ✅ Multi-layer inference routing
- ✅ Comprehensive test suite (93%+ passing)
- ✅ Security controls (Gatekeeper)

Areas still in development:
- Fine-tuned telemetry and cost optimization
- Advanced agent capabilities (web search, transcription)
- Production-grade monitoring and alerting

---

## Still Have Questions?

Check the comprehensive documentation:
- **Master Manual:** `READ_ME_GRAVITAS_MASTER_MANUAL.md`
- **Architecture:** `docs/000_MASTER_OVERVIEW.md` through `005_development_protocols.md`
- **Roadmap:** `docs/ROADMAP.md`
- **Test Guide:** `docs/TEST_GUIDE.md`

Or ask Gravitas directly through the Nexus Dashboard!
