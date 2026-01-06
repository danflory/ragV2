# 007: MODEL GOVERNANCE & DYNAMIC ROUTING

**Version:** 6.0.0  
**Status:** Active  
**Last Updated:** 2026-01-05

---

## OVERVIEW

The **Gravitas Supervisor** is a standalone FastAPI proxy service that intelligently routes inference requests across a three-tier model architecture. It prevents VRAM thrashing, manages request queuing, and optimizes for cost, speed, and capability.

### Core Principles

1. **Zero-Cost Privacy First (L1):** Default to local models whenever possible
2. **Disruption Avoidance:** Queue management prevents model thrashing
3. **Intelligent Offloading:** Route complex tasks to appropriate tiers
4. **Observable Performance:** Shadow-audit loop tracks all routing decisions
5. **Certified Safety:** No model can be routed without a valid Wrapper Certificate

---

## ARCHITECTURE

### Three-Tier Model System

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT REQUEST                            │
│                  (OpenAI-compatible)                         │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  GRAVITAS SUPERVISOR  │
         │   (Port 8000)         │
         │                       │
         │  ┌─────────────────┐ │
         │  │ Dispatcher      │ │
         │  │ Router          │ │
         │  └────────┬────────┘ │
         │           │          │
         │    ┌──────┴──────┐  │
         │    │   Decision   │  │
         │    │   Engine     │  │
         │    └──────┬───────┘  │
         └───────────┼──────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
    ┌──────┐    ┌──────┐    ┌──────┐
    │  L1  │    │  L2  │    │  L3  │
    │LOCAL │    │CLOUD │    │GEMINI│
    └──────┘    └──────┘    └──────┘
```

### Tier Definitions

#### L1: Local Intelligence (Ollama)
- **Cost:** $0.00 per request
- **Privacy:** 100% local, no data leaves the machine
- **Models:** `gemma2:27b`, `llama3:70b`, `qwen2.5-coder:32b`
- **VRAM:** GPU 0 (Titan RTX, 24GB)
- **Latency:** 50-500ms (warm model)
- **Use Cases:** General queries, RAG operations, standard coding

#### L2: Specialized Cloud (DeepInfra)
- **Cost:** $0.0007 - $0.0020 per 1K tokens
- **Privacy:** Encrypted transit, third-party processing
- **Models:** `meta-llama/Meta-Llama-3-70B-Instruct`, specialized agents
- **Latency:** 200-800ms
- **Use Cases:** High load offloading, specialized tasks, large-scale summarization

#### L3: Frontier Intelligence (Gemini)
- **Cost:** $0.01 per 1K tokens (1.5 Pro)
- **Context:** Up to 2M tokens
- **Models:** `gemini-1.5-pro`, `gemini-1.5-flash`
- **Latency:** 1-5 seconds
- **Use Cases:** Complex reasoning, massive context analysis, code architecture review

---

## DISPATCHER LOGIC

### Routing Rules (Priority Order)

```python
# Rule A: Complexity Threshold
if query.code_complexity > 8:
    → Route to L3 (Gemini 1.5 Pro)
    
# Rule B: System Load Protection  
elif telemetry.system_load_percent > 90:
    → Route to L2 (DeepInfra)
    
# Rule C: Default Path
else:
    → Route to L1 (Local Ollama)
```

### Decision Matrix

| Condition | Complexity | VRAM Load | System Load | → Tier |
|-----------|------------|-----------|-------------|--------|
| Complex reasoning | >8 | Any | Any | **L3** |
| High system strain | Any | Any | >90% | **L2** |
| Standard operation | ≤8 | <80% | <90% | **L1** |
| VRAM exhausted | Any | >95% | Any | **L2** |

---

## QUEUE MANAGEMENT (L1 ORBIT)

### Purpose
Prevent "context thrashing" where rapid model switching causes continuous VRAM load/unload cycles that can take 30-60 seconds per switch.

### Queue Strategy

```python
class RequestQueue:
    """
    Priority queue with FIFO preservation for equal priorities.
    
    Priority Levels:
        -1: Mr. Big Guy (Emergency/User Override)
         0: High Priority (System Critical)
        10: Standard Priority (Default)
        20: Low Priority (Background Tasks)
    """
```

### Model Lock Protocol

```python
class ModelLock:
    """
    Tracks the currently loaded ("HOT") model in VRAM.
    
    States:
        - None: No model loaded
        - "gemma2:27b": Gemma currently hot
        - "llama3:70b": Llama currently hot
    """
```

### Queue Behavior

**Scenario 1: Same Model**
```
Hot Model: gemma2:27b
Incoming Request: gemma2:27b
→ Process immediately (no queue)
```

**Scenario 2: Different Model (Queue Active)**
```
Hot Model: gemma2:27b (Queue: 3 requests pending)
Incoming Request: llama3:70b
→ Enqueue llama3 request
→ Continue processing gemma2 queue
→ After gemma2 queue depletes, switch to llama3
```

**Scenario 3: Mr. Big Guy Override**
```
Hot Model: gemma2:27b (Queue: 5 requests)
Incoming: llama3:70b with priority=-1
→ Flush current queue politely
→ Switch to llama3 immediately
→ Re-queue pending gemma2 requests with priority 20
```

---

## API CLIENTS

### DeepInfra Client

**Endpoint:** `https://api.deepinfra.com/v1/openai/chat/completions`

**Authentication:**
```bash
export DEEPINFRA_API_KEY="your_key_here"
```

**Request Format:**
```json
{
  "model": "meta-llama/Meta-Llama-3-70B-Instruct",
  "messages": [
    {"role": "user", "content": "Summarize this document..."}
  ],
  "temperature": 0.7
}
```

**Features:**
- OpenAI-compatible API
- Automatic retry with exponential backoff
- Graceful fallback on API failure
- Connection timeout: 30 seconds

### Gemini Client

**Endpoint:** `https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent`

**Authentication:**
```bash
export GOOGLE_API_KEY="your_key_here"
```

**Request Format:**
```json
{
  "contents": [
    {
      "parts": [
        {"text": "Analyze this entire codebase..."}
      ]
    }
  ]
}
```

**Features:**
- Native Gemini format with OpenAI compatibility layer
- 60-second timeout for large context operations
- Response format conversion to OpenAI schema
- Error logging and graceful degradation

---

## WRAPPER CERTIFICATION & GUARDIAN

Before an agent can be registered in the routing system, it must pass a dual validation process ensuring it complies with the **Reasoning Pipe** protocol.

### Certification Flow
```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│  Wrapper Code   │─────▶│ WrapperCertifier │─────▶│ JSON Certificate│
│ (Implementation)│      │ (Static/Dynamic) │      │ (app/.certs/)   │
└─────────────────┘      └──────────────────┘      └────────┬────────┘
                                                            │
                                                            ▼
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│     Client      │─────▶│ Gravitas         │─────▶│ Supervisor      │
│     Request     │      │ Supervisor       │      │ Guardian        │
└─────────────────┘      └──────────────────┘      └────────┬────────┘
                                                            │
                                                            ▼
                                                   { Verify Signature }
                                                            │
                                                   ┌────────┴────────┐
                                                   │      ALLOW      │
                                                   └─────────────────┘
```

1. **Static Analysis**: Certifier checks for inheritance from `GravitasAgentWrapper` and implementation of required abstract methods (`_execute_internal`, `_parse_thought`).
2. **Dynamic Validation**: Certifier executes a test task and validates the generated `ReasoningPipe` markdown for format compliance and content fidelity.
3. **Guardian Enforcement**: Upon every task execution, the `SupervisorGuardian` verifies that the agent has a non-expired certificate before allowing the session to start.

---

## AGENT REGISTRY

Formal catalog of available models with capability metadata:

```python
AGENT_REGISTRY = {
    "L1": {
        "gemma2:27b": {
            "cost_per_1k_tokens": 0.0,
            "context_window": 8192,
            "vram_required_gb": 16,
            "avg_latency_ms": 150,
            "capabilities": ["general", "rag", "summarization"],
            "specialty": None
        },
        "llama3:70b": {
            "cost_per_1k_tokens": 0.0,
            "context_window": 8192,
            "vram_required_gb": 42,
            "avg_latency_ms": 800,
            "capabilities": ["reasoning", "analysis", "complex_tasks"],
            "specialty": None
        },
        "qwen2.5-coder:32b": {
            "cost_per_1k_tokens": 0.0,
            "context_window": 32768,
            "vram_required_gb": 20,
            "avg_latency_ms": 300,
            "capabilities": ["code", "debugging", "refactoring"],
            "specialty": "coding"
        }
    },
    "L2": {
        "meta-llama/Meta-Llama-3-70B-Instruct": {
            "cost_per_1k_tokens": 0.0007,
            "context_window": 8192,
            "avg_latency_ms": 400,
            "capabilities": ["general", "analysis", "summarization"],
            "specialty": None,
            "provider": "deepinfra"
        }
    },
    "L3": {
        "gemini-1.5-pro": {
            "cost_per_1k_tokens": 0.01,
            "context_window": 2000000,
            "avg_latency_ms": 2500,
            "capabilities": ["advanced_reasoning", "massive_context", "code_review"],
            "specialty": "frontier_intelligence",
            "provider": "google"
        },
        "gemini-1.5-flash": {
            "cost_per_1k_tokens": 0.002,
            "context_window": 1000000,
            "avg_latency_ms": 800,
            "capabilities": ["fast_reasoning", "large_context"],
            "specialty": "speed",
            "provider": "google"
        }
    }
}
```

---

## SHADOW-AUDIT LOOP

**Purpose:** Build a dataset of routing decisions for future autonomous optimization.

### Telemetry Logged Per Request

```python
{
    "request_id": "uuid",
    "timestamp": "2026-01-05T21:45:32Z",
    "complexity_estimated": 7,
    "telemetry_snapshot": {
        "vram_usage_percent": 45.2,
        "system_load_percent": 23.1,
        "avg_latency_ms": 150.3
    },
    "routing_decision": {
        "tier": "L1",
        "model": "gemma2:27b",
        "reasoning": "Default route (complexity ≤8, load normal)"
    },
    "actual_performance": {
        "latency_ms": 145.7,
        "tokens_generated": 342,
        "success": true,
        "cost": 0.0
    },
    "deviation": {
        "expected_latency_ms": 150.0,
        "latency_delta_ms": -4.3,
        "prediction_accuracy": 97.1
    }
}
```

### Storage
- **Location:** `Gravitas_postgres.routing_audit` table
- **Retention:** 60 days (aligned with telemetry policy)
- **Aggregation:** Daily summary statistics for trend analysis

### Future Use Cases
1. **Self-Optimization:** ML model trained on routing decisions
2. **Cost Analysis:** Total spend per tier over time
3. **Performance Benchmarking:** Actual vs. predicted latency
4. **Failure Pattern Detection:** Identify models with high error rates

---

## DOCKER INTEGRATION

### Service Definition

```yaml
gravitas_supervisor:
  build:
    context: ./gravitas_supervisor
  container_name: gravitas_supervisor
  ports:
    - "8000:8000"
  environment:
    - OLLAMA_URL=http://Gravitas_ollama:11434/v1/chat/completions
    - DEEPINFRA_API_KEY=${DEEPINFRA_API_KEY}
    - GOOGLE_API_KEY=${GOOGLE_API_KEY}
  depends_on:
    - ollama
  networks:
    - Gravitas_net
  restart: unless-stopped
```

### Health Check

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "queue_size": 3,
  "hot_model": "gemma2:27b",
  "uptime_seconds": 3600
}
```

---

## PERFORMANCE BENCHMARKS

### Target Latencies

| Operation | L1 (Local) | L2 (DeepInfra) | L3 (Gemini) |
|-----------|------------|----------------|-------------|
| Simple query (50 tokens) | <200ms | <400ms | <1000ms |
| RAG context (500 tokens) | <500ms | <800ms | <2000ms |
| Code analysis (2K tokens) | <2s | <3s | <5s |
| Large context (50K tokens) | N/A | <30s | <60s |

### Cost Efficiency

**Monthly Budget Example (10K requests):**
- 100% L1: **$0.00**
- 80% L1, 15% L2, 5% L3: **~$15.00**
- 50% L1, 30% L2, 20% L3: **~$65.00**

---

## TESTING REQUIREMENTS

### Unit Tests (Completed ✅)
- `test_queue_logic.py` - Priority and FIFO behavior
- `test_model_lock.py` - VRAM tracking
- `test_dispatcher_router.py` - Routing rule validation

### Integration Tests (Required)

#### L1 Queue Management Test
```python
async def test_l1_queue_persistence():
    """
    Verify that incoming Model B requests queue properly
    when Model A is hot with active queue.
    """
```

#### L2 Specialist Test
```python
async def test_l2_deepinfra_specialists():
    """
    1. Document Summarization (General Analyst)
    2. Code Problem Solving (Coding Specialist)
    """
```

#### L3 Accountant's Audit Test
```python
async def test_l3_full_repo_audit():
    """
    Gather ALL project files and prompt Gemini 1.5 Pro
    for comprehensive 8-page architectural critique.
    """
```

---

## MIGRATION GUIDE

### Updating Existing Code

**Before (Direct Ollama):**
```python
import httpx
response = await httpx.post(
    "http://localhost:11434/v1/chat/completions",
    json={"model": "gemma2", "messages": messages}
)
```

**After (Via Supervisor):**
```python
import httpx
response = await httpx.post(
    "http://localhost:8000/v1/chat/completions",
    json={
        "model": "gemma2", 
        "messages": messages,
        "complexity": 5  # Optional: routing hint
    }
)
```

The supervisor maintains OpenAI compatibility while adding intelligent routing.

---

## OPERATIONAL GUIDELINES

### When to Override Routing

Use `complexity` parameter to influence routing:
```python
# Force high-tier routing
{"complexity": 10}  # → L3 (Gemini)

# Ensure local processing
{"complexity": 1}   # → L1 (Ollama)
```

### Monitoring

1. **Queue Depth:** Monitor `/health` endpoint
2. **Hot Model:** Track VRAM utilization via telemetry
3. **Routing Decisions:** Query `routing_audit` table
4. **Cost Tracking:** Daily aggregation of L2/L3 usage

### Debugging

**Enable verbose logging:**
```bash
export LOG_LEVEL=DEBUG
docker-compose restart gravitas_supervisor
docker logs -f gravitas_supervisor
```

---

## FUTURE ENHANCEMENTS

### Phase 5.5 (Planned)
- [ ] Automatic failover between L2 providers
- [ ] Cost-aware routing with daily budget caps
- [ ] Real-time model performance tracking
- [ ] A/B testing framework for routing rules

### Phase 6 Integration (Active)
- [x] Reasoning Pipe integration for routing decisions
- [x] Wrapper Certification enforcement
- [x] Standardized journaling via `ReasoningPipe` library
- [ ] Self-learning routing optimization (Phase 7)

---

## REFERENCES

- **Phase 4.5:** Granular Telemetry Calibration (`006_telemetry_calibration.md`)
- **Phase 1:** Qdrant & MinIO Infrastructure (`002_vector_memory.md`)
- **Hardware Spec:** Dual-GPU Operations (`004_hardware_operations.md`)
- **Testing Protocols:** Development Standards (`005_development_protocols.md`)

---

**Document Owner:** Gravitas Grounded Research  
**Review Cycle:** Every phase completion  
**Next Review:** Phase 6 completion
