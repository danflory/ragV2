# Architecture: Thinking Transparency & Cognitive Telemetry

## 1. Executive Summary: From Chore to Emergence
The current challenge is that "Thinking Transparency" is treated as a **manual literary task** (asking agents to write journals), which fails on lower-tier models (L1/L2) due to lack of reasoning depth.

**The Solution:** Shift from **Active Journaling** to **Cognitive Telemetry**.
Instead of asking an agent to "write a thought," we require them to **emit a structured signal** (a "Thought Beacon") for every significant state change. The system then aggregates these signals into a readable narrative.

## 2. The Mechanics: Cognitive Telemetry
We decouple the **experience** of the agent from the **reporting** of the agent.

### The "Thought Tunnel" Decorator
Every agent method (e.g., `search`, `summarize`) is wrapped in a decorator that captures:
1.  **Input Intent**: What are we trying to do?
2.  **Structural Output**: What did we get?
3.  **State Tag**: What is the "Truth Level"?

This ensures that even if an L1 model cannot write a poem about its failure, the **Structure** of the failure is captured and logged automatically.

## 3. The "Truth Logic" Schema
To solve the "Hallucination vs. Fact" problem, L1/L2 agents must tag their internal states with a strict **Truth Level**.

| Level | Tag | Definition | Log Destiny |
| :--- | :--- | :--- | :--- |
| **L1** | `[GROUNDED]` | Direct observation (e.g., "File not found", "API 200"). Fact. | Session Log (Debug) |
| **L2** | `[INFERRED]` | Logical deduction (e.g., "Since X is null, Y must be skipped"). Reasoning. | Session Log (Audit) |
| **L3** | `[STRATEGIC]` | High-level planning or hypothesis (e.g., "Pivoting search strategy"). Intent. | **Main Journal (thoughts.md)** |

**The Protocol:**
- Agents emit JSON signals: `{"level": "INFERRED", "content": "Skipping file..."}`.
- A "Cortex" listener filters these signals. Only `[STRATEGIC]` signals are promoted to the main `thoughts.md` file.

## 4. Solving the Volume Crossroads: Fractal Logging
**The Problem:** High-volume agents (Scout scraping 50 pages) create too much noise for a human reader.
**The Solution:** Fractal Logging.

1.  **The Session Log (The Leaves)**:
    - File: `logs/sessions/scout_run_849.log`
    - Content: FULL telemetry (Every `[GROUNDED]` and `[INFERRED]` signal).
    - Audience: Forensic Deep-Dive (only read when things break).

2.  **The Main Journal (The Trunk)**:
    - File: `docs/journals/YYYY-MM-DD_thoughts.md`
    - Content: Only `[STRATEGIC]` signals and "Anomalies" (unexpected failures).
    - Audience: Human Supervisors and L3 Agents.

## 5. Implementation Strategy
We do not retrain L1s. We simply enforce a JSON output schema or wrap their tools.

```python
# The "Truth" Object
class ThoughtBeacon(BaseModel):
    agent_id: str
    truth_level: Literal["GROUNDED", "INFERRED", "STRATEGIC"]
    confidence: float
    message: str
    context_snapshot: dict
```

## 6. Conclusion
By automating the *collection* of thoughts via telemetry and filtering them via Truth Logic, "Transparency" becomes a system constant, not a task variable. The human sees a clean narrative (The Trunk) but retains the ability to zoom into the microscopic actions (The Leaves) instantly.
