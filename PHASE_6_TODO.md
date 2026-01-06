# PHASE 6: REASONING PIPES IMPLEMENTATION TODO

**Target**: Enable wrapper certification for Claude Sonnet 4.5 Thinking, Gemini 2.0 Flash Thinking, Qwen2.5-Coder (DeepInfra), codellama:7b (Ollama), and other local Ollama models.

**Architecture**: Wrapper Certification Model (Supervisor validates code, agents write pipes)

---

## PRIORITY 1: CORE INFRASTRUCTURE

### Task 1.1: ReasoningPipe Standard Library
**File**: `app/lib/reasoning_pipe.py`

**Requirements**:
1. Create `ReasoningPipe` class with the following methods:
   - `__init__(agent_name: str, session_id: str, model: str, tier: str)`
     - Initialize session metadata
     - Create buffer for in-memory logging
     - Generate output path: `docs/journals/ReasoningPipe_{agent_name}_{session_id}.md`
   
   - `log_thought(content: str, timestamp: Optional[datetime] = None) -> None`
     - Append to buffer: `**[HH:MM:SS.mmm]** THOUGHT: {content}`
     - Auto-generate timestamp if not provided (use `datetime.now()`)
     - Validate content is non-empty string
   
   - `log_action(action: str, details: Optional[dict] = None) -> None`
     - Append to buffer: `**[HH:MM:SS.mmm]** ACTION: {action}`
     - If details provided, format as: `ACTION: {action} (key1: val1, key2: val2)`
     - Common details: `confidence`, `alternatives`, `cost`
   
   - `log_result(result: str, metrics: Optional[dict] = None) -> None`
     - Append to buffer: `**[HH:MM:SS.mmm]** RESULT: {result}`
     - Store metrics for session metadata (tokens, duration, cost)
   
   - `finalize() -> Path`
     - Write buffer to file with full markdown template (see below)
     - Append summary line to `docs/journals/ReasoningPipe_{agent_name}.md`
     - Return Path to written file
     - Clear buffer after write

2. **Markdown Template** (use this exact format):
```markdown
# ReasoningPipe: {agent_name} | Session: {session_id}

**Started**: {ISO8601_timestamp}  
**Model**: {model_name}  
**Tier**: {L1|L2|L3}  
**Task**: {task_description if provided}

---

## Thought Stream

{buffer_contents_here}

---

## Session Metadata

**Duration**: {duration}s  
**Tokens Generated**: {tokens}  
**Efficiency**: {tokens_per_second} tok/s  
**Cost**: ${cost} ({tier})  
**Finalized**: {ISO8601_timestamp}
```

3. **Error Handling**:
   - If `docs/journals/` doesn't exist, create it
   - If file write fails, raise `ReasoningPipeWriteError` with path
   - If `finalize()` called twice, log warning and return existing path

4. **Dependencies**:
   - `from datetime import datetime`
   - `from pathlib import Path`
   - `from typing import Optional, Dict`
   - `import json`

**Test Coverage Required**:
- Test each method independently
- Test full workflow: init → log_thought → log_action → log_result → finalize
- Test timestamp auto-generation
- Test file creation in `docs/journals/`
- Test error handling (write failures, double finalize)

**Tie-in**: This is the foundation that ALL wrappers will use. Must be robust and well-tested before proceeding to Task 1.2.

---

### Task 1.2: Supervisor Guardian (Session Manager)
**File**: `app/services/supervisor/guardian.py`

**Requirements**:
1. Create `SupervisorGuardian` class:
   - `__init__()`
     - Load certificates from `app/.certificates/` directory
     - Initialize `active_sessions` dict: `{session_id: metadata}`
     - Log startup message with count of loaded certificates
   
   - `_load_certificates() -> Dict[str, Certificate]`
     - Read all JSON files in `app/.certificates/`
     - Parse each as: `{"agent_name": str, "issued_at": ISO8601, "expires_at": ISO8601, "signature": str}`
     - Return dict mapping agent_name → Certificate
     - If dir doesn't exist, create it and return empty dict
   
   - `notify_session_start(agent: str, session_id: str, metadata: dict) -> SessionPermission`
     - Check if agent in `self.certified_agents`
     - If not: raise `AgentNotCertifiedError(f"{agent} not certified")`
     - Check if certificate expired: `datetime.fromisoformat(cert.expires_at) < datetime.now()`
     - If expired: raise `CertificationExpiredError(f"{agent} cert expired at {expires_at}")`
     - If valid: Add to `active_sessions` with: `{session_id: {agent, started_at, status: "active", metadata}}`
     - Return `SessionPermission(allowed=True, reason="Certified")`
   
   - `notify_session_end(session_id: str, output_file: Path) -> None`
     - Find session in `active_sessions`
     - Update: `status = "completed"`, `ended_at = datetime.now()`, `output_file = str(output_file)`
     - Calculate duration: `ended_at - started_at`
     - Log completion message with agent name, session_id, duration
   
   - `get_session_stats(agent: Optional[str] = None) -> dict`
     - If agent specified: return stats for that agent
     - Else: return stats for all agents
     - Format: `{"agent_name": {"active_sessions": int, "completed_today": int, "certification_expires": ISO8601}}`

2. **Custom Exceptions**:
   - `class AgentNotCertifiedError(Exception): pass`
   - `class CertificationExpiredError(Exception): pass`

3. **Certificate Storage**:
   - Location: `app/.certificates/{agent_name}.json`
   - Format: `{"agent_name": "Scout", "issued_at": "2026-01-05T22:00:00Z", "expires_at": "2026-02-05T22:00:00Z", "version": "1.0", "signature": "sha256_hash"}`

**Test Coverage Required**:
- Test certificate loading from directory
- Test session_start with valid cert
- Test session_start with missing cert (should raise error)
- Test session_start with expired cert (should raise error)
- Test session_end updates status correctly
- Test get_session_stats aggregation

**Tie-in**: Wrappers call `notify_session_start()` before execution and `notify_session_end()` after. This enforces certification without touching the data flow.

---

### Task 1.3: Base Wrapper Class
**File**: `app/wrappers/base_wrapper.py`

**Requirements**:
1. Create abstract base class `GravitasAgentWrapper`:
   - `__init__(agent_name: str, session_id: str, model: str, tier: str)`
     - Store all parameters as instance variables
     - Create `self.pipe = ReasoningPipe(agent_name, session_id, model, tier)`
     - Create `self.supervisor = SupervisorGuardian()`
   
   - `async def execute_task(task: dict) -> dict` (DO NOT OVERRIDE)
     - Call `permission = await self.supervisor.notify_session_start(self.agent_name, self.session_id, {"task": task})`
     - If not `permission.allowed`: raise `RuntimeError(permission.reason)`
     - Call `result = await self._execute_internal(task)` (subclass implements this)
     - Call `pipe_file = self.pipe.finalize()`
     - Call `await self.supervisor.notify_session_end(self.session_id, pipe_file)`
     - Return result
   
   - `@abstractmethod async def _execute_internal(task: dict) -> dict`
     - Subclass must implement
     - Should call `self.pipe.log_thought()`, `self.pipe.log_action()`, `self.pipe.log_result()`
   
   - `@abstractmethod def _parse_thought(chunk: dict) -> Optional[str]`
     - Model-specific parsing of reasoning content
   
   - `@abstractmethod def _parse_action(chunk: dict) -> Optional[str]`
     - Model-specific parsing of action declarations

2. **Dependencies**:
   - `from abc import ABC, abstractmethod`
   - `from typing import Optional, Dict`
   - `from app.lib.reasoning_pipe import ReasoningPipe`
   - `from app.services.supervisor.guardian import SupervisorGuardian`

**Test Coverage Required**:
- Test that execute_task enforces supervisor protocol
- Test that uncertified agent is rejected
- Test that subclass must implement abstract methods

**Tie-in**: All wrapper implementations (Tasks 2.1-2.4) will inherit from this class. It handles 90% of the protocol automatically.

---

## PRIORITY 2: WRAPPER IMPLEMENTATIONS

### Task 2.1: Gemini 2.0 Flash Thinking Wrapper
**File**: `app/wrappers/gemini_wrapper.py`

**Requirements**:
1. Inherit from `GravitasAgentWrapper`
2. `__init__(session_id: str, api_key: Optional[str] = None)`
   - Call `super().__init__("Gemini_Thinking", session_id, "gemini-2.0-flash-thinking-exp", "L3")`
   - Initialize Google Generative AI client:
     ```python
     import google.generativeai as genai
     genai.configure(api_key=api_key or os.getenv("GOOGLE_API_KEY"))
     self.client = genai.GenerativeModel(self.model)
     ```

3. `async def _execute_internal(task: dict) -> dict`
   - Extract prompt: `prompt = task.get("prompt")`
   - Stream response:
     ```python
     response = await self.client.generate_content_async(prompt, stream=True)
     full_output = []
     async for chunk in response:
         thought = self._parse_thought(chunk)
         if thought:
             self.pipe.log_thought(thought)
         
         if chunk.text:
             full_output.append(chunk.text)
     
     result = "".join(full_output)
     self.pipe.log_result(f"Generated {len(result)} chars", {"tokens": len(result) // 4})
     return {"output": result}
     ```

4. `def _parse_thought(chunk: dict) -> Optional[str]`
   - Gemini 2.0 Flash Thinking has a `thinking` field in chunks
   - Return `chunk.thinking if hasattr(chunk, 'thinking') else None`

5. `def _parse_action(chunk: dict) -> Optional[str]`
   - Gemini doesn't have explicit action markers
   - Return `None`

**Environment Setup**:
- Requires: `GOOGLE_API_KEY` in `.env`
- Install: `pip install google-generativeai`

**Test Task**: "Explain the concept of 'gravitas' in one paragraph"
**Expected Output**: ReasoningPipe file with multiple THOUGHT entries showing Gemini's reasoning process

**Tie-in**: This is the L3 reasoning model. Its THOUGHT logs will be high-quality chain-of-thought traces for future training data.

---

### Task 2.2: Claude Sonnet 4.5 Thinking Wrapper
**File**: `app/wrappers/claude_wrapper.py`

**Requirements**:
1. Inherit from `GravitasAgentWrapper`
2. `__init__(session_id: str, api_key: Optional[str] = None)`
   - Call `super().__init__("Claude_Thinking", session_id, "claude-sonnet-4-5-thinking", "L3")`
   - Initialize Anthropic client:
     ```python
     from anthropic import AsyncAnthropic
     self.client = AsyncAnthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
     ```

3. `async def _execute_internal(task: dict) -> dict`
   - Extract prompt: `prompt = task.get("prompt")`
   - Stream response:
     ```python
     response = await self.client.messages.create(
         model=self.model,
         messages=[{"role": "user", "content": prompt}],
         max_tokens=4096,
         stream=True
     )
     
     full_output = []
     async for chunk in response:
         thought = self._parse_thought(chunk)
         if thought:
             self.pipe.log_thought(thought)
         
         if chunk.type == "content_block_delta" and chunk.delta.text:
             full_output.append(chunk.delta.text)
     
     result = "".join(full_output)
     self.pipe.log_result(f"Generated {len(result)} chars", {"tokens": len(result) // 4})
     return {"output": result}
     ```

4. `def _parse_thought(chunk: dict) -> Optional[str]`
   - Claude Sonnet 4.5 uses `<thinking>` tags in the response text
   - Parse with regex:
     ```python
     import re
     if chunk.type == "content_block_delta" and chunk.delta.text:
         match = re.search(r'<thinking>(.*?)</thinking>', chunk.delta.text, re.DOTALL)
         return match.group(1).strip() if match else None
     return None
     ```

5. `def _parse_action(chunk: dict) -> Optional[str]`
   - Claude doesn't have explicit action markers
   - Return `None`

**Environment Setup**:
- Requires: `ANTHROPIC_API_KEY` in `.env`
- Install: `pip install anthropic`

**Test Task**: "Analyze the theological significance of 'gravitas'"
**Expected Output**: ReasoningPipe file with THOUGHT entries from `<thinking>` tags

**Tie-in**: Claude's reasoning is verbose and high-quality. This will provide excellent training data for theological analysis tasks.

---

### Task 2.3: Ollama Local Models Wrapper
**File**: `app/wrappers/ollama_wrapper.py`

**Requirements**:
1. Inherit from `GravitasAgentWrapper`
2. `__init__(session_id: str, model_name: str, ollama_url: str = "http://localhost:11434")`
   - Call `super().__init__(f"Ollama_{model_name}", session_id, model_name, "L1")`
   - Store `self.ollama_url = ollama_url`

3. `async def _execute_internal(task: dict) -> dict`
   - Extract prompt: `prompt = task.get("prompt")`
   - Stream response from Ollama API:
     ```python
     import httpx
     import json
     
     async with httpx.AsyncClient(timeout=120.0) as client:
         async with client.stream(
             "POST",
             f"{self.ollama_url}/api/generate",
             json={"model": self.model, "prompt": prompt, "stream": True}
         ) as response:
             full_output = []
             async for line in response.aiter_lines():
                 if not line:
                     continue
                 chunk = json.loads(line)
                 
                 thought = self._parse_thought(chunk)
                 if thought:
                     self.pipe.log_thought(thought)
                 
                 action = self._parse_action(chunk)
                 if action:
                     self.pipe.log_action(action)
                 
                 if chunk.get("response"):
                     full_output.append(chunk["response"])
             
             result = "".join(full_output)
             self.pipe.log_result(f"Generated {len(result)} chars", {"tokens": chunk.get("total_tokens", 0)})
             return {"output": result}
     ```

4. `def _parse_thought(chunk: dict) -> Optional[str]`
   - Parse custom `<think>` tags (if model uses them):
     ```python
     import re
     text = chunk.get("response", "")
     match = re.search(r'<think>(.*?)</think>', text, re.DOTALL)
     return match.group(1).strip() if match else None
     ```

5. `def _parse_action(chunk: dict) -> Optional[str]`
   - Parse custom `<action>` tags:
     ```python
     import re
     text = chunk.get("response", "")
     match = re.search(r'<action>(.*?)</action>', text, re.DOTALL)
     return match.group(1).strip() if match else None
     ```

**Environment Setup**:
- Requires: Ollama running on localhost:11434
- Models to test: `codellama:7b`, `qwen2.5:7b`, `llama3:8b`

**Test Task**: "Write a Python function to calculate factorial"
**Expected Output**: ReasoningPipe file with THOUGHT/ACTION entries if model uses tags, otherwise just RESULT

**Tie-in**: This wrapper supports ANY Ollama model by passing model_name. Enables rapid experimentation with new local models.

---

### Task 2.4: DeepInfra (Qwen2.5-Coder) Wrapper
**File**: `app/wrappers/deepinfra_wrapper.py`

**Requirements**:
1. Inherit from `GravitasAgentWrapper`
2. `__init__(session_id: str, model_name: str = "Qwen/Qwen2.5-Coder-32B-Instruct", api_key: Optional[str] = None)`
   - Call `super().__init__(f"DeepInfra_{model_name.split('/')[-1]}", session_id, model_name, "L2")`
   - Initialize OpenAI-compatible client:
     ```python
     from openai import AsyncOpenAI
     self.client = AsyncOpenAI(
         api_key=api_key or os.getenv("DEEPINFRA_API_KEY"),
         base_url="https://api.deepinfra.com/v1/openai"
     )
     ```

3. `async def _execute_internal(task: dict) -> dict`
   - Extract prompt: `prompt = task.get("prompt")`
   - Stream response:
     ```python
     response = await self.client.chat.completions.create(
         model=self.model,
         messages=[{"role": "user", "content": prompt}],
         stream=True,
         max_tokens=4096
     )
     
     full_output = []
     async for chunk in response:
         delta = chunk.choices[0].delta
         
         # For reasoning models, early chunks might be CoT
         if delta.content:
             # Log first 3 chunks as potential reasoning
             if len(full_output) < 3:
                 self.pipe.log_thought(f"Processing: {delta.content[:50]}...")
             
             full_output.append(delta.content)
     
     result = "".join(full_output)
     self.pipe.log_result(f"Generated {len(result)} chars", {"tokens": len(result) // 4})
     return {"output": result}
     ```

4. `def _parse_thought(chunk: dict) -> Optional[str]`
   - DeepInfra doesn't expose native thinking output
   - Return `None`

5. `def _parse_action(chunk: dict) -> Optional[str]`
   - DeepInfra doesn't have action markers
   - Return `None`

**Environment Setup**:
- Requires: `DEEPINFRA_API_KEY` in `.env`
- Install: `pip install openai` (OpenAI SDK works with DeepInfra)

**Test Task**: "Refactor this code to use async/await: [simple sync code]"
**Expected Output**: ReasoningPipe file with minimal THOUGHT entries (first 3 chunks) and RESULT

**Tie-in**: Qwen2.5-Coder is L2 (cost-effective coding tasks). This enables comparison between L1 (codellama local) vs L2 (Qwen cloud) vs L3 (Gemini/Claude).

---

## PRIORITY 3: CERTIFICATION SYSTEM

### Task 3.1: Wrapper Certifier (Static + Dynamic Validation)
**File**: `app/services/supervisor/certifier.py`

**Requirements**:
1. Create `WrapperCertifier` class:
   - `async def certify_wrapper(wrapper_path: str, agent_name: str) -> CertificationResult`
     - Run 3 validation steps:
       1. Static analysis: `_static_analysis(wrapper_path)`
       2. Dynamic test: `_dynamic_test(wrapper_path, agent_name)`
       3. Output validation: `_validate_output(expected_pipe_file)`
     - If all pass: Issue certificate with `_issue_certificate(agent_name, wrapper_path)`
     - Return `CertificationResult(approved=True/False, errors=List[str], certificate=Optional[Certificate])`
   
   - `def _static_analysis(wrapper_path: str) -> AnalysisResult`
     - Read file contents
     - Check imports: `"from app.wrappers.base_wrapper import GravitasAgentWrapper"` present
     - Check class definition: Class inherits from `GravitasAgentWrapper`
     - Check methods: `_execute_internal`, `_parse_thought`, `_parse_action` defined
     - Return `AnalysisResult(passed=True/False, errors=List[str])`
   
   - `async def _dynamic_test(wrapper_path: str, agent_name: str) -> TestResult`
     - Import wrapper module dynamically:
       ```python
       import importlib.util
       spec = importlib.util.spec_from_file_location("wrapper", wrapper_path)
       module = importlib.util.module_from_spec(spec)
       spec.loader.exec_module(module)
       wrapper_class = getattr(module, "GeminiWrapper")  # Or detect class name
       ```
     - Instantiate wrapper with test session_id: `test_session_id = f"cert_test_{uuid.uuid4()}"`
     - Run test task: `result = await wrapper.execute_task({"prompt": "Summarize the word 'gravitas'"})`
     - Check no exceptions raised
     - Return `TestResult(passed=True/False, errors=List[str], session_id=test_session_id)`
   
   - `def _validate_output(pipe_file: Path) -> ValidationResult`
     - Check file exists: `pipe_file.exists()`
     - Read file contents
     - Validate markdown structure:
       - Header: `# ReasoningPipe: {agent} | Session: {session_id}`
       - Metadata: `**Started**:`, `**Model**:`, `**Tier**:`
       - Thought stream section: `## Thought Stream`
       - At least one entry: `**[HH:MM:SS.mmm]** THOUGHT:` or `**[HH:MM:SS.mmm]** RESULT:`
       - Session metadata: `## Session Metadata`
       - Finalized timestamp: `**Finalized**:`
     - Return `ValidationResult(passed=True/False, errors=List[str])`
   
   - `def _issue_certificate(agent_name: str, wrapper_path: str) -> Certificate`
     - Calculate SHA-256 hash of wrapper file:
       ```python
       import hashlib
       with open(wrapper_path, 'rb') as f:
           file_hash = hashlib.sha256(f.read()).hexdigest()
       ```
     - Create certificate:
       ```python
       cert = {
           "agent_name": agent_name,
           "issued_at": datetime.now().isoformat(),
           "expires_at": (datetime.now() + timedelta(days=30)).isoformat(),
           "version": "1.0",
           "signature": file_hash
       }
       ```
     - Write to: `app/.certificates/{agent_name}.json`
     - Return `Certificate(**cert)`

2. **CLI Interface**:
   - Add `if __name__ == "__main__":` block:
     ```python
     import argparse
     parser = argparse.ArgumentParser()
     parser.add_argument("--certify", help="Path to wrapper to certify")
     parser.add_argument("--agent-name", help="Agent name for certificate")
     parser.add_argument("--list", action="store_true", help="List all certified agents")
     args = parser.parse_args()
     
     certifier = WrapperCertifier()
     if args.certify:
         result = asyncio.run(certifier.certify_wrapper(args.certify, args.agent_name))
         print(result)
     elif args.list:
         # List all certs in app/.certificates/
     ```

**Test Coverage Required**:
- Test static analysis detects missing imports
- Test static analysis detects missing methods
- Test dynamic test runs successfully with valid wrapper
- Test output validation catches malformed pipe files
- Test certificate issuance creates correct JSON

**Tie-in**: This is the gatekeeper. No wrapper can be used in production without passing certification.

---

### Task 3.2: Monthly Auditor
**File**: `app/services/supervisor/auditor.py`

**Requirements**:
1. Create `ReasoningPipeAuditor` class:
   - `async def monthly_audit() -> AuditReport`
     - Get list of all certified agents from `app/.certificates/`
     - For each agent:
       - Get ReasoningPipe files from last 30 days: `docs/journals/ReasoningPipe_{agent}_*.md`
       - Score quality: `score = _audit_quality(pipe_files)`
       - If score < 75: Flag for re-certification
     - Return `AuditReport(agents_audited=int, flagged_agents=List[str])`
   
   - `def _audit_quality(pipe_files: List[Path]) -> QualityScore`
     - Scoring criteria (100 points total):
       - **Format compliance (40 pts)**: Valid markdown, timestamps, metadata present
       - **Completeness (30 pts)**: THOUGHT/ACTION/RESULT entries present
       - **Efficiency (20 pts)**: Tokens/second within acceptable range (10-100 tok/s)
       - **Cost accuracy (10 pts)**: Cost calculations match expected tier costs
     - Return `QualityScore(total=int, breakdown=dict)`
   
   - `async def _flag_for_recertification(agent: str, reason: str)`
     - Load certificate from `app/.certificates/{agent}.json`
     - Update: `cert["status"] = "pending_review"`
     - Add: `cert["audit_flag"] = {"flagged_at": now, "reason": reason}`
     - Write back to file
     - Log warning message

2. **CLI Interface**:
   - Add `if __name__ == "__main__":` block for manual audit trigger

**Test Coverage Required**:
- Test quality scoring logic
- Test flagging low-quality agents
- Test audit report generation

**Tie-in**: Ensures wrappers maintain quality over time. Prevents "certification drift" where agents stop following protocol.

---

## PRIORITY 4: TESTING

### Task 4.1: Specification Tests
**File**: `tests/test_spec_008_reasoning_pipes.py`

**Requirements**:
Create test classes for each component:

1. `TestReasoningPipeClass`:
   - `test_init_creates_proper_paths()`
   - `test_log_thought_adds_to_buffer()`
   - `test_log_action_formats_details()`
   - `test_log_result_stores_metrics()`
   - `test_finalize_writes_file()`
   - `test_finalize_creates_directory_if_missing()`
   - `test_double_finalize_warning()`

2. `TestSupervisorGuardian`:
   - `test_load_certificates_from_directory()`
   - `test_notify_session_start_with_valid_cert()`
   - `test_notify_session_start_rejects_uncertified()`
   - `test_notify_session_start_rejects_expired()`
   - `test_notify_session_end_updates_status()`
   - `test_get_session_stats_aggregation()`

3. `TestBaseWrapper`:
   - `test_execute_task_calls_supervisor()`
   - `test_execute_task_enforces_certification()`
   - `test_abstract_methods_must_be_implemented()`

4. `TestWrapperCertifier`:
   - `test_static_analysis_detects_missing_imports()`
   - `test_static_analysis_detects_inheritance()`
   - `test_dynamic_test_runs_wrapper()`
   - `test_output_validation_checks_format()`
   - `test_issue_certificate_creates_file()`

5. `TestReasoningPipeAuditor`:
   - `test_audit_quality_scoring()`
   - `test_flag_for_recertification()`

**Run Command**: `pytest tests/test_spec_008_reasoning_pipes.py -v`

**Tie-in**: These tests validate the infrastructure before wrappers are built. Must pass 100% before moving to Task 4.2.

---

### Task 4.2: Wrapper Certification Tests
**File**: `tests/test_wrapper_certification.py`

**Requirements**:
1. `TestGeminiWrapperCertification`:
   - `test_gemini_wrapper_certifies_successfully()`
   - `test_gemini_wrapper_produces_valid_pipe()`
   - `test_gemini_wrapper_handles_api_errors()`

2. `TestClaudeWrapperCertification`:
   - `test_claude_wrapper_certifies_successfully()`
   - `test_claude_wrapper_parses_thinking_tags()`
   - `test_claude_wrapper_produces_valid_pipe()`

3. `TestOllamaWrapperCertification`:
   - `test_ollama_wrapper_certifies_successfully()`
   - `test_ollama_wrapper_supports_multiple_models()`
   - `test_ollama_wrapper_produces_valid_pipe()`

4. `TestDeepInfraWrapperCertification`:
   - `test_deepinfra_wrapper_certifies_successfully()`
   - `test_deepinfra_wrapper_produces_valid_pipe()`

**Run Command**: `pytest tests/test_wrapper_certification.py -v`

**Tie-in**: These tests validate that each wrapper passes the certification process. This is the acceptance criteria for Phase 6.

---

### Task 4.3: End-to-End Integration Tests
**File**: `tests/integration/test_reasoning_pipe_e2e.py`

**Requirements**:
1. `test_full_certification_workflow()`:
   - Certify a wrapper
   - Execute a task
   - Verify ReasoningPipe file created
   - Verify session tracked by Guardian
   - Verify file format correct

2. `test_multi_agent_concurrent_execution()`:
   - Run Gemini and Claude wrappers simultaneously
   - Verify separate ReasoningPipe files created
   - Verify no session ID collisions

3. `test_uncertified_agent_rejection()`:
   - Try to execute wrapper without certification
   - Verify `AgentNotCertifiedError` raised

4. `test_expired_certificate_rejection()`:
   - Manually expire a certificate (set `expires_at` to past)
   - Try to execute wrapper
   - Verify `CertificationExpiredError` raised

5. `test_performance_overhead()`:
   - Measure execution time with ReasoningPipe logging
   - Measure execution time without logging
   - Verify overhead < 5%

**Run Command**: `pytest tests/integration/test_reasoning_pipe_e2e.py -v`

**Tie-in**: These tests validate the entire system works end-to-end in a production-like environment.

---

## PRIORITY 5: DOCUMENTATION

### Task 5.1: Wrapper Development Guide
**File**: `docs/WRAPPER_DEVELOPMENT_GUIDE.md`

**Requirements**:
Create a developer-friendly guide with:
1. **Introduction**: What is a wrapper, why certification is required
2. **Quick Start**: Copy-paste template for new wrapper
3. **Step-by-Step Tutorial**:
   - Inherit from `GravitasAgentWrapper`
   - Implement `_execute_internal()`
   - Implement `_parse_thought()` and `_parse_action()`
   - Test locally
   - Run certification: `python app/services/supervisor/certifier.py --certify ...`
4. **Best Practices**:
   - Error handling
   - Timeout management
   - Cost tracking
5. **Troubleshooting**:
   - Common certification failures
   - How to debug pipe output
6. **Examples**:
   - Link to existing wrappers (Gemini, Claude, Ollama, DeepInfra)

**Tie-in**: This enables rapid onboarding of new models. With this guide, adding a new model should take < 1 hour.

---

### Task 5.2: Update Existing Specs
**Files**: `docs/005_development_protocols.md`, `docs/007_model_governance.md`

**Requirements**:
1. **005_development_protocols.md** → v6.0.0:
   - Add section: "Reasoning Pipe Protocol"
   - Reference wrapper certification requirement
   - Add to development workflow: "Before deploying agent, run certification"

2. **007_model_governance.md** → v6.0.0:
   - Update "Agent Integration" section
   - Reference wrapper certification as prerequisite for Supervisor routing
   - Add diagram showing certification flow

**Tie-in**: Keeps all documentation synchronized. Ensures developers understand how Phase 6 integrates with Phase 5.

---

## COMPLETION CHECKLIST

### Infrastructure (Priority 1)
- [x] Task 1.1: ReasoningPipe library implemented and tested
- [x] Task 1.2: SupervisorGuardian implemented and tested
- [x] Task 1.3: Base wrapper class implemented and tested

### Wrappers (Priority 2)
- [x] Task 2.1: Gemini wrapper certified
- [x] Task 2.2: Claude wrapper certified
- [x] Task 2.3: Ollama wrapper certified (test with codellama:7b)
- [x] Task 2.4: DeepInfra wrapper certified (Qwen2.5-Coder)

### Certification System (Priority 3)
- [x] Task 3.1: Certifier implemented with CLI
- [x] Task 3.2: Auditor implemented with CLI

### Testing (Priority 4)
- [x] Task 4.1: Specification tests → 100% pass
- [x] Task 4.2: Wrapper certification tests → 100% pass
- [x] Task 4.3: E2E integration tests → 100% pass

### Documentation (Priority 5)
- [ ] Task 5.1: Wrapper development guide complete
- [x] Task 5.2: Existing specs updated to v6.0.0

### Final Verification
```bash
# Run all tests
pytest tests/ -v

# Certify all wrappers
python app/services/supervisor/certifier.py --certify app/wrappers/gemini_wrapper.py --agent-name Gemini_Thinking
python app/services/supervisor/certifier.py --certify app/wrappers/claude_wrapper.py --agent-name Claude_Thinking
python app/services/supervisor/certifier.py --certify app/wrappers/ollama_wrapper.py --agent-name Ollama_codellama
python app/services/supervisor/certifier.py --certify app/wrappers/deepinfra_wrapper.py --agent-name DeepInfra_Qwen2.5-Coder

# List certified agents
python app/services/supervisor/certifier.py --list
# Expected: 4 agents with valid certificates

# Generate test ReasoningPipe files
python -c "
from app.wrappers.gemini_wrapper import GeminiWrapper
import asyncio
wrapper = GeminiWrapper('test_001')
asyncio.run(wrapper.execute_task({'prompt': 'Summarize gravitas'}))
"

# Verify output
ls -lh docs/journals/ReasoningPipe_*.md
cat docs/journals/ReasoningPipe_Gemini_Thinking_test_001.md
```

---

## SUCCESS CRITERIA

Phase 6 is **COMPLETE** when:
1. ✅ All 4 wrappers certified (Gemini, Claude, Ollama, DeepInfra)
2. ✅ Test suite: 100% pass rate (40+ tests)
3. ✅ Performance: ReasoningPipe logging < 5% overhead
4. ✅ Documentation: Developer guide enables <1 hour new wrapper creation
5. ✅ Real ReasoningPipe files generated with valid format
6. ✅ Monthly audit runs successfully on existing pipes

**Expected Timeline**: 
- Priority 1 (Infrastructure): 4-6 hours
- Priority 2 (Wrappers): 6-8 hours (2 hours per wrapper)
- Priority 3 (Certification): 4-6 hours
- Priority 4 (Testing): 4-6 hours
- Priority 5 (Documentation): 2-3 hours
**Total**: 20-29 hours of focused development

---

## NOTES FOR FLASH MODEL CODER

1. **Dependencies**: Install before starting:
   ```bash
   pip install google-generativeai anthropic openai httpx pytest
   ```

2. **Environment Variables**: Required in `.env`:
   ```
   GOOGLE_API_KEY=your_gemini_key
   ANTHROPIC_API_KEY=your_claude_key
   DEEPINFRA_API_KEY=your_deepinfra_key
   ```

3. **Docker Consideration**: All wrappers should work both locally and in Docker. Use environment variables for API keys.

4. **Error Handling**: Every wrapper must handle:
   - Network timeouts
   - API rate limits
   - Invalid responses
   - Model unavailability

5. **Testing Strategy**: Test each component independently before integration. Use pytest fixtures for common setup.

6. **Code Style**: Follow PEP 8, use type hints, add docstrings to all public methods.

7. **Git Workflow**: Commit after each task completion. Use descriptive commit messages referencing task numbers.

---

**END OF TODO**
