# Debug Plan & Architecture Handoff: Supervisor Service (V2)

## Goal
Stabilize the Supervisor service by fixing the `ModuleNotFoundError` and perform a critical architectural evaluation of its responsibilities to prevent future "Monolithic Agent" burnout.

---

## 1. Immediate Fix: Dependency Mismatch
**Status**: Fix Applied, Build Interrupted.

### The Issue
- **Error**: `ModuleNotFoundError: No module named 'google.generativeai'`
- **Cause**: `requirements.txt` incorrectly requested `google-genai` (deprecated/different package) instead of `google-generativeai`.

### The Fix
- **File**: `requirements.txt`
- **Change**: Replaced `google-genai` with `google-generativeai>=0.8.3`.
- **Validation**: Verified locally via `venv/bin/python` that `import google.generativeai` now works.

### Action Item: Resume Docker Build
The build was interrupted during image export. The `pip install` layer is cached, so this will be fast.
```bash
docker-compose up -d --build gravitas_supervisor gravitas_mcp gravitas_lobby
```
*Verify success by checking logs for "Uvicorn running on...".*

---

## 2. Verification Steps (Post-Build)
Once the service is running:

1.  **Health Check**:
    ```bash
    curl http://localhost:8000/health
    ```
2.  **Smoke Test**:
    ```bash
    docker exec gravitas_mcp pytest tests/integration/test_phase7_security.py::test_supervisor_health
    ```

---

## 3. Think Outside the Box: Is Supervisor "Overworked"?
**Architectural Critique Request**

The recent instability suggests the **Supervisor** might be taking on too many responsibilities, becoming a bottleneck or a "God Object."

**Current Responsibilities:**
1.  **Routing** (L1/L2/L3 decision logic)
2.  **Provider Management** (Ollama, Gemini, DeepInfra clients)
3.  **Security Enforcement** (Policy Engine, Audit Logging)
4.  **Identity Management** (JWT generation/validation)
5.  **Agent Certification** (Guardian logic)

**Risk**: If the Supervisor process crashes (e.g., bad import), *everything* stops.

### Proposal for Evaluation: "Supervisor Helpers"
Please evaluate decomposing the Supervisor into specialized micro-services or independent "Helper Agents":

1.  **The Gatekeeper (Security Helper)**:
    - Handles JWTs, Policy Checks, and Audit Logging.
    - Sits *in front* of the Supervisor?
    - *Benefit*: Routing logic changes won't break security.

2.  **The Router (Traffic Helper)**:
    - Purely decides "Where does this prompt go?"
    - No execution logic, just dispatch.
    - *Benefit*: Extremely lightweight and stable.

3.  **The Guardian (Certification Helper)**:
    - Manages the Ledger and Certificates.
    - *Benefit*: Isolate state management from high-frequency inference traffic.

**Question for Next Agent**:
*Should we refactor the Supervisor into these smaller, more resilient components to improve system stability and dev velocity?*
