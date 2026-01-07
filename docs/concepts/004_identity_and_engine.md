# THE GHOST AND THE SHELL: IDENTITY VS. ENGINE

> **Architectural Concept**: In Gravitas Enterprise, an "Employee" (Agent) is a permanent **Identity** that "wears" a swappable **Cognitive Engine** (Brain).

---

## 1. The Separation of Church and State
You asked: *"Each employee has its brain assigned one to one... [and] get to be swapped once a month."*

This is the **Core Driver** of Gravitas evolvability.

*   **The Identity (The Ghost):** "The Librarian."
    *   **Attributes:** Responsibilities, Knowledge Access, Permissions, Personality.
    *   **Continuity:** This persists forever.
*   **The Engine (The Shell):** "Gemini 2.0 Flash."
    *   **Attributes:** IQ, Speed, Cost, Context Window.
    *   **Transience:** This is swapped out endlessly as technology improves.

**The Power:**
We can upgrade **The Librarian** from *Llama 3* to *Llama 4* without changing the Librarian's job description, just like upgrading an employee's laptop.

---

## 2. Silicon Brains vs. Steel Gears (Models vs. Tools)
You also noted: *"Some employee brains are actually not brains but fast automation."*

This is the distinction between **Probabilistic** and **Deterministic** agents.

### **Type A: The Thinker (Probabilistic)**
*   **Engine:** LLM (Gemini, Claude, Llama).
*   **Nature:** "Brain."
*   **Mechanism:** Reads text, understands context, makes a judgment call.
*   **Margin of Error:** Non-Zero (can hallucinate).
*   **Role:** The Author, The Scout, The Judge.

### **Type B: The Machine (Deterministic)**
*   **Engine:** Python Scripts / Regex / Graph Algorithms.
*   **Nature:** "Tool."
*   **Mechanism:** If X, then Y. Always.
*   **Margin of Error:** Zero (if code is bug-free).
*   **Role:** The Transcriber (Miner), The Syntax Validator, The Scheduler.

---

## 3. The Enterprise "Org Chart"

In the future Agent Registry, an entry looks like this:

```yaml
Agent: GravitasLibarian
  - Role: Curator of Truth
  - Current Brain: gemma2:27b (Swapped from llama3 on Jan 2026)
  - Backup Brain: deepinfra/qwen2.5-coder
  - Allowed Tools: [Neo4j_Write, Qdrant_Upsert]

Agent: GravitasMiner
  - Role: Excavator
  - Current Brain: None (Pure Python Automation)
  - Core Driver: /scripts/youtube_dl.py
  - Allowed Tools: [Write_Local_File]
```

This confirms your model: **Function is Permanent. Intelligence is Swappable.**
