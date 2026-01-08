# 008: REASONING PIPES & WRAPPER CERTIFICATION

**Version**: 6.0.0  
**Status**: Active Development  
**Phase**: 6 - Self-Learning Data  
**Last Updated**: 2026-01-05

---

## EXECUTIVE SUMMARY

Phase 6 establishes the **Reasoning Pipe Protocol**: a standardized method for capturing chain-of-thought (CoT) traces from reasoning models in real-time. Unlike centralized token interception, this architecture uses **wrapper certification** where the Supervisor validates agent code compliance rather than processing data streams.

### Core Principles:
1. **Agents own their data flow** - No centralized token bottleneck
2. **Supervisor validates wrappers** - Certification-based enforcement
3. **Model-agnostic normalization** - Each wrapper handles its model's format
4. **Self-learning foundation** - ReasoningPipes become training data

---

## ARCHITECTURE OVERVIEW

```
┌──────────────────────────────────────────────────────────────┐
│                  WRAPPER CERTIFICATION MODEL                  │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────┐         ┌──────────────────┐          │
│  │   Supervisor    │         │  Agent Wrapper   │          │
│  │   (Certifier)   │────────▶│  (Self-Contained)│          │
│  │                 │         │                  │          │
│  │ • Pre-validates │         │ • Parses model   │          │
│  │ • Issues cert   │         │ • Writes pipe    │          │
│  │ • Tracks state  │         │ • Normalizes CoT │          │
│  │ • Audits output │         │ • Self-manages   │          │
│  └─────────────────┘         └──────────────────┘          │
│                                                              │
│  Flow:                                                       │
│  1. Developer submits wrapper → Supervisor validates        │
│  2. Supervisor issues 30-day certificate                    │
│  3. Wrapper executes (direct model access, no proxy)        │
│  4. Wrapper writes ReasoningPipe_{agent}_{session}.md       │
│  5. Monthly audit: Supervisor reviews output quality        │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## COMPONENT SPECIFICATIONS

### 1. ReasoningPipe Standard Library

**Location**: `app/lib/reasoning_pipe.py`

**Purpose**: Standardized interface that all agent wrappers must use.

**Core Methods**:
```python
class ReasoningPipe:
    def __init__(self, agent_name: str, session_id: str, model: str, tier: str):
        """
        Initialize a new reasoning pipe for a session.
        
        Args:
            agent_name: Name of the agent (e.g., "Scout", "Librarian")
            session_id: Unique session identifier (UUID)
            model: Model identifier (e.g., "gemini-1.5-pro", "llama3:70b")
            tier: Execution tier (L1/L2/L3)
        """
        
    def log_thought(self, content: str, timestamp: Optional[datetime] = None):
        """
        Log a reasoning/thinking step.
        
        Args:
            content: The thought content (model's internal reasoning)
            timestamp: Optional timestamp (auto-generated if not provided)
        """
        
    def log_action(self, action: str, details: Optional[dict] = None):
        """
        Log a concrete action taken by the agent.
        
        Args:
            action: Action description (e.g., "Escalate to L3", "Query Qdrant")
            details: Optional metadata (confidence, alternatives, cost, etc.)
        """
        
    def log_result(self, result: str, metrics: Optional[dict] = None):
        """
        Log the final result of a task.
        
        Args:
            result: Result description
            metrics: Performance metrics (tokens, duration, cost)
        """
        
    def finalize(self) -> Path:
        """
        Finalize the session and write to permanent storage.
        
        Returns:
            Path to the written ReasoningPipe file
            
        Behavior:
            1. Writes buffer to: docs/journals/ReasoningPipe_{agent}_{session}.md
            2. Appends summary to: docs/journals/ReasoningPipe_{agent}.md
            3. Notifies Supervisor of session completion
        """
```

**File Format Standard**:
```markdown
# ReasoningPipe: {agent_name} | Session: {session_id}

**Started**: {ISO8601_timestamp}  
**Model**: {model_identifier}  
**Tier**: {L1|L2|L3}  
**Task**: {task_description}

---

## Thought Stream

**[HH:MM:SS.mmm]** THOUGHT: {reasoning_content}  
**[HH:MM:SS.mmm]** ACTION: {action_description} (confidence: {0.0-1.0})  
**[HH:MM:SS.mmm]** RESULT: {outcome_description}

---

## Session Metadata

**Duration**: {seconds}s  
**Tokens Generated**: {count}  
**Efficiency**: {tokens/second}  
**Cost**: ${amount} ({tier})  
**Finalized**: {ISO8601_timestamp}
```

---

### 2. Supervisor Certifier

**Location**: `app/services/supervisor/certifier.py`

**Purpose**: Validates agent wrappers before deployment.

**Certification Process**:

```python
class WrapperCertifier:
    """
    Pre-deployment validation of agent wrappers.
    """
    
    async def certify_wrapper(
        self, 
        wrapper_path: str,
        agent_name: str
    ) -> CertificationResult:
        """
        Full certification pipeline.
        
        Steps:
        1. Static Analysis: Check code structure
        2. Dynamic Testing: Run test task
        3. Output Validation: Verify ReasoningPipe format
        4. Certificate Issuance: Sign and store
        
        Returns:
            CertificationResult with approval status and errors
        """
        
    def _static_analysis(self, wrapper_path: str) -> AnalysisResult:
        """
        Checks:
        - Imports ReasoningPipe from app.lib.reasoning_pipe
        - Implements required methods (execute_task, _parse_thought, _parse_action)
        - Calls supervisor.notify_session_start/end
        - Calls pipe.finalize()
        """
        
    def _dynamic_test(self, wrapper: AgentWrapper) -> TestResult:
        """
        Runs standardized test task:
        - Simple query: "Summarize the word 'gravitas'"
        - Expected output: ReasoningPipe file with:
            * Thought entries
            * Action entries (if any)
            * Result entry
            * Valid metadata
        """
        
    def _validate_output(self, pipe_file: Path) -> ValidationResult:
        """
        Checks:
        - File exists at expected path
        - Markdown format correct
        - Timestamps in chronological order
        - Metadata complete (duration, tokens, cost)
        - Finalization timestamp present
        """
        
    def _issue_certificate(self, agent_name: str) -> Certificate:
        """
        Creates certificate:
        {
            "agent_name": "Scout",
            "issued_at": "2026-01-05T22:30:00Z",
            "expires_at": "2026-02-05T22:30:00Z",
            "version": "1.0",
            "signature": "sha256_hash_of_wrapper_code"
        }
        
        Stored in: app/.certificates/{agent_name}.json
        """
```

**Certification Command**:
```bash
# CLI for wrapper certification
python app/services/supervisor/certifier.py \
    --certify app/wrappers/scout_wrapper.py \
    --agent-name Scout
```

---

### 3. Supervisor Guardian

**Location**: `app/services/supervisor/guardian.py`

**Purpose**: Runtime enforcement of certification requirements.

```python
class SupervisorGuardian:
    """
    Enforces that only certified agents can execute.
    """
    
    def __init__(self):
        self.certified_agents = self._load_certificates()
        self.active_sessions = {}  # {session_id: session_metadata}
        
    async def notify_session_start(
        self, 
        agent: str, 
        session_id: str,
        metadata: dict
    ) -> SessionPermission:
        """
        Called by agent wrapper before task execution.
        
        Validation:
        1. Agent has valid certificate?
        2. Certificate not expired?
        3. No existing session conflicts?
        
        Returns:
            SessionPermission(allowed=True/False, reason=str)
            
        Raises:
            AgentNotCertifiedError: If agent lacks certification
            CertificationExpiredError: If cert expired
        """
        
    async def notify_session_end(
        self, 
        session_id: str,
        output_file: Path
    ):
        """
        Called by agent wrapper after pipe.finalize().
        
        Actions:
        1. Mark session as completed
        2. Queue for quality audit
        3. Update session statistics
        """
        
    def get_session_stats(self, agent: Optional[str] = None) -> dict:
        """
        Returns session statistics for monitoring.
        
        Response:
        {
            "Scout": {
                "active_sessions": 2,
                "completed_today": 45,
                "avg_duration": 8.3,
                "certification_expires": "2026-02-05T22:30:00Z"
            }
        }
        """
```

---

### 4. Supervisor Auditor

**Location**: `app/services/supervisor/auditor.py`

**Purpose**: Monthly quality audits of agent output.

```python
class ReasoningPipeAuditor:
    """
    Post-hoc quality validation of ReasoningPipe output.
    """
    
    async def monthly_audit(self):
        """
        Runs on the 1st of each month.
        
        For each certified agent:
        1. Collect last 30 days of ReasoningPipe files
        2. Score output quality (format compliance, completeness)
        3. Flag agents below threshold for re-certification
        """
        
    def _audit_quality(self, pipe_files: List[Path]) -> QualityScore:
        """
        Scoring criteria:
        - Format compliance: 40 points (valid markdown, timestamps, metadata)
        - Completeness: 30 points (thoughts, actions, results present)
        - Efficiency: 20 points (tokens/second within norms)
        - Cost accuracy: 10 points (cost calculations correct)
        
        Total: 100 points
        Threshold: 75 points (below triggers re-certification)
        """
        
    async def _flag_for_recertification(
        self, 
        agent: str, 
        reason: str
    ):
        """
        Actions:
        1. Send notification to Nexus Dashboard
        2. Mark certificate as "pending_review"
        3. Allow existing sessions to complete
        4. Block new session starts until re-certified
        """
```

---

## AGENT WRAPPER STANDARD

### Base Wrapper Interface

**Location**: `app/wrappers/base_wrapper.py`

```python
from abc import ABC, abstractmethod
from app.lib.reasoning_pipe import ReasoningPipe
from app.services.supervisor.guardian import SupervisorGuardian

class GravitasAgentWrapper(ABC):
    """
    Base class all agent wrappers must inherit from.
    
    Implements 90% of the protocol, leaving only model-specific
    parsing to the subclass.
    """
    
    def __init__(self, agent_name: str, session_id: str, model: str, tier: str):
        self.agent_name = agent_name
        self.session_id = session_id
        self.model = model
        self.tier = tier
        
        self.pipe = ReasoningPipe(agent_name, session_id, model, tier)
        self.supervisor = SupervisorGuardian()
        
    async def execute_task(self, task: dict) -> dict:
        """
        Standard execution flow (DO NOT OVERRIDE).
        """
        # 1. Request permission
        permission = await self.supervisor.notify_session_start(
            agent=self.agent_name,
            session_id=self.session_id,
            metadata={"task": task, "model": self.model}
        )
        
        if not permission.allowed:
            raise RuntimeError(f"Session rejected: {permission.reason}")
        
        # 2. Execute (model-specific)
        result = await self._execute_internal(task)
        
        # 3. Finalize
        pipe_file = self.pipe.finalize()
        await self.supervisor.notify_session_end(
            session_id=self.session_id,
            output_file=pipe_file
        )
        
        return result
    
    @abstractmethod
    async def _execute_internal(self, task: dict) -> dict:
        """
        Model-specific execution logic.
        
        Must call:
        - self.pipe.log_thought() for reasoning steps
        - self.pipe.log_action() for concrete actions
        - self.pipe.log_result() for final output
        """
        pass
    
    @abstractmethod
    def _parse_thought(self, chunk: dict) -> Optional[str]:
        """
        Extract reasoning content from model response chunk.
        
        Model-specific examples:
        - Gemini: chunk.get('thinking')
        - Claude: Parse <thinking>...</thinking> tags
        - Ollama: Parse custom <think> tags
        - DeepSeek: Extract CoT markers
        """
        pass
    
    @abstractmethod
    def _parse_action(self, chunk: dict) -> Optional[str]:
        """
        Extract action declarations from model response.
        """
        pass
```

---

### Wrapper Examples

#### Example 1: Gemini Wrapper

**Location**: `app/wrappers/gemini_wrapper.py`

```python
from app.wrappers.base_wrapper import GravitasAgentWrapper
from google import generativeai as genai

class GeminiWrapper(GravitasAgentWrapper):
    """
    Wrapper for Gemini 2.0 Flash Thinking models (L3).
    """
    
    def __init__(self, session_id: str):
        super().__init__(
            agent_name="Gemini_Agent",
            session_id=session_id,
            model="gemini-2.0-flash-thinking-exp",
            tier="L3"
        )
        self.client = genai.GenerativeModel(self.model)
        
    async def _execute_internal(self, task: dict) -> dict:
        prompt = task.get("prompt")
        
        # Stream response
        response = await self.client.generate_content_async(
            prompt,
            stream=True
        )
        
        full_output = []
        async for chunk in response:
            # Gemini thinking models have a 'thinking' field
            thought = self._parse_thought(chunk)
            if thought:
                self.pipe.log_thought(thought)
            
            # Regular content
            if chunk.text:
                full_output.append(chunk.text)
        
        result = "".join(full_output)
        self.pipe.log_result(
            result=f"Generated {len(result)} chars",
            metrics={
                "tokens": len(result) // 4,  # Rough estimate
                "duration": 5.2  # From response metadata
            }
        )
        
        return {"output": result}
    
    def _parse_thought(self, chunk: dict) -> Optional[str]:
        """Gemini-specific thinking extraction."""
        if hasattr(chunk, 'thinking'):
            return chunk.thinking
        return None
    
    def _parse_action(self, chunk: dict) -> Optional[str]:
        """Gemini doesn't have explicit action markers."""
        return None
```

#### Example 2: Ollama Wrapper

**Location**: `app/wrappers/ollama_wrapper.py`

```python
from app.wrappers.base_wrapper import GravitasAgentWrapper
import httpx
import re

class OllamaWrapper(GravitasAgentWrapper):
    """
    Wrapper for local Ollama models (L1).
    """
    
    def __init__(self, session_id: str, model_name: str):
        super().__init__(
            agent_name=f"Ollama_{model_name}",
            session_id=session_id,
            model=model_name,
            tier="L1"
        )
        self.ollama_url = "http://localhost:11434/api/generate"
        
    async def _execute_internal(self, task: dict) -> dict:
        prompt = task.get("prompt")
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.ollama_url,
                json={"model": self.model, "prompt": prompt, "stream": True}
            )
            
            full_output = []
            async for line in response.aiter_lines():
                chunk = json.loads(line)
                
                # Parse thinking tags
                thought = self._parse_thought(chunk)
                if thought:
                    self.pipe.log_thought(thought)
                
                # Parse action tags
                action = self._parse_action(chunk)
                if action:
                    self.pipe.log_action(action)
                
                # Regular content
                if chunk.get("response"):
                    full_output.append(chunk["response"])
            
            result = "".join(full_output)
            self.pipe.log_result(
                result=f"Generated {len(result)} chars",
                metrics={"tokens": chunk.get("total_tokens", 0)}
            )
            
            return {"output": result}
    
    def _parse_thought(self, chunk: dict) -> Optional[str]:
        """Extract <think>...</think> tags."""
        text = chunk.get("response", "")
        match = re.search(r'<think>(.*?)</think>', text, re.DOTALL)
        return match.group(1).strip() if match else None
    
    def _parse_action(self, chunk: dict) -> Optional[str]:
        """Extract <action>...</action> tags."""
        text = chunk.get("response", "")
        match = re.search(r'<action>(.*?)</action>', text, re.DOTALL)
        return match.group(1).strip() if match else None
```

#### Example 3: DeepInfra Wrapper

**Location**: `app/wrappers/deepinfra_wrapper.py`

```python
from app.wrappers.base_wrapper import GravitasAgentWrapper
from openai import AsyncOpenAI

class DeepInfraWrapper(GravitasAgentWrapper):
    """
    Wrapper for DeepInfra models (L2).
    """
    
    def __init__(self, session_id: str, model_name: str):
        super().__init__(
            agent_name=f"DeepInfra_{model_name.split('/')[-1]}",
            session_id=session_id,
            model=model_name,
            tier="L2"
        )
        self.client = AsyncOpenAI(
            api_key=os.getenv("DEEPINFRA_API_KEY"),
            base_url="https://api.deepinfra.com/v1/openai"
        )
        
    async def _execute_internal(self, task: dict) -> dict:
        prompt = task.get("prompt")
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )
        
        full_output = []
        async for chunk in response:
            delta = chunk.choices[0].delta
            
            # DeepInfra doesn't have native thinking output,
            # but we can log the streaming process
            if delta.content:
                # For reasoning models, first chunks might be CoT
                if len(full_output) < 3:  # First few chunks likely reasoning
                    self.pipe.log_thought(f"Processing: {delta.content[:50]}...")
                
                full_output.append(delta.content)
        
        result = "".join(full_output)
        self.pipe.log_result(
            result=f"Generated {len(result)} chars",
            metrics={"tokens": len(result) // 4}
        )
        
        return {"output": result}
    
    def _parse_thought(self, chunk: dict) -> Optional[str]:
        """DeepInfra has no explicit thinking field."""
        return None
    
    def _parse_action(self, chunk: dict) -> Optional[str]:
        """DeepInfra has no explicit action field."""
        return None
```

---

## CERTIFICATION REQUIREMENTS

### Checklist for All Wrappers

To pass certification, a wrapper must:

- [ ] **Inherit from `GravitasAgentWrapper`**
- [ ] **Implement `_execute_internal()`**
- [ ] **Implement `_parse_thought()`** (return `None` if model doesn't support)
- [ ] **Implement `_parse_action()`** (return `None` if model doesn't support)
- [ ] **Call `self.pipe.log_thought()` at least once per task**
- [ ] **Call `self.pipe.log_result()` exactly once per task**
- [ ] **NOT override `execute_task()`** (base class handles supervisor protocol)
- [ ] **Handle errors gracefully** (network failures, model timeouts)
- [ ] **Pass test task**: "Summarize the word 'gravitas'" in < 30 seconds
- [ ] **Produce valid ReasoningPipe markdown file**

---

## PHASE 6 DELIVERABLES

### Code Deliverables

1. **`app/lib/reasoning_pipe.py`** - Standard library
2. **`app/services/supervisor/certifier.py`** - Certification logic
3. **`app/services/supervisor/guardian.py`** - Runtime enforcement
4. **`app/services/supervisor/auditor.py`** - Monthly quality audits
5. **`app/wrappers/base_wrapper.py`** - Abstract base class
6. **`app/wrappers/gemini_wrapper.py`** - Gemini 2.0 Flash Thinking
7. **`app/wrappers/ollama_wrapper.py`** - Local Ollama models
8. **`app/wrappers/deepinfra_wrapper.py`** - DeepInfra models
9. **`app/wrappers/claude_wrapper.py`** - Claude Sonnet 4.5 Thinking

### Test Deliverables

10. **`tests/test_spec_008_reasoning_pipes.py`** - Specification tests
11. **`tests/test_wrapper_certification.py`** - Certification process tests
12. **`tests/integration/test_reasoning_pipe_e2e.py`** - End-to-end tests

### Documentation Deliverables

13. **`docs/008_reasoning_pipes.md`** - This specification (✓)
14. **`docs/WRAPPER_DEVELOPMENT_GUIDE.md`** - Developer guide
15. **Phase 6 completion summary**

---

## SECURITY CONSIDERATIONS

### Certificate Integrity

Certificates use SHA-256 hash of wrapper source code:
- Any modification to wrapper invalidates certificate
- Re-certification required after code changes
- Prevents malicious wrapper modifications post-approval

### Sandbox Execution (Future)

Phase 6.5 consideration:
- Run wrapper certification tests in isolated containers
- Prevent malicious code execution during validation
- Use resource limits (CPU, memory, network)

---

## PERFORMANCE BENCHMARKS

### Target Metrics

| Metric | Target | Rationale |
|--------|--------|-----------|
| Certification time | < 60 seconds | Fast feedback for developers |
| ReasoningPipe file size | < 500 KB/session | Prevent disk bloat |
| Log overhead | < 5% latency | Minimal performance impact |
| Monthly audit | < 10 minutes | Scalable to 100+ agents |

---

## FUTURE ENHANCEMENTS

### Phase 6.5: Advanced Analytics

- **Reasoning Quality Scoring**: LLM-based evaluation of thought coherence
- **Cost Optimization**: Identify when L3 was unnecessarily used
- **A/B Testing**: Compare model performance on identical tasks
- **Anomaly Detection**: Flag unusual reasoning patterns

### Phase 7 Integration

- **Knowledge Graph**: Extract entities from ReasoningPipes
- **Librarian Training**: Use pipes to fine-tune summarization models
- **Scout Learning**: Build context retrieval training set

---

## APPENDIX: CLI COMMANDS

### Certification
```bash
# Certify a new wrapper
python app/services/supervisor/certifier.py \
    --certify app/wrappers/my_wrapper.py \
    --agent-name MyAgent

# List all certified agents
python app/services/supervisor/certifier.py --list

# Check certificate status
python app/services/supervisor/certifier.py \
    --status MyAgent
```

### Auditing
```bash
# Run monthly audit manually
python app/services/supervisor/auditor.py --audit

# Audit specific agent
python app/services/supervisor/auditor.py \
    --audit-agent Scout

# View audit history
python app/services/supervisor/auditor.py --history
```

### Testing
```bash
# Test wrapper without certification
python app/services/supervisor/certifier.py \
    --test-only app/wrappers/my_wrapper.py

# Validate ReasoningPipe file format
python app/lib/reasoning_pipe.py \
    --validate docs/journals/ReasoningPipe_Scout_abc123.md
```

---

**END OF SPECIFICATION**
