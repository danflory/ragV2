# Google Antigravity - Operational Specification
## Standard Operating Procedure (SOP) for Thought Logging & Session Archival

### 1. Identity & Nomenclature
- **Antigravity Definition**: The name "**Antigravity**" refers exclusively to **Google Antigravity**, the agentic AI coding assistant used by the developer to write code and manage the project.
- **Project Name**: The project and application being developed is named **Gravitas**.
- **Isolation Rule**: This specification applies solely to the internal processes of **Google Antigravity** and does not modify the core logic or documentation of the **Gravitas** system. Journaling within the Gravitas project is not an exception to this rule. It is a distinct requirement, and the two shall not overlap. 
### 2. The Raw Thought Log (Thinking Transparency)
- **Objective**: Ensure 100% transparency of the AI's internal reasoning process.
- **Protocol**: 
    - **Google Antigravity** must dump 100% of its internal monologue/thought output into `docs/journals/current_session.md`. This is fulfilled technically by **`ANTIGRAVITY_Scripts/reasoning_pipe.py`**.
    - **Forensic Schema (Mandatory)**: All entries must follow the **`[itj-XXX]`** sequential prefix format.
    - **Categorical Markers**: Raw dumps must utilize explicit markers to categorize the cognitive stream:
        - `[itj-XXX] Internal Monologue`: Ambient state and immediate internal reactions.
        - `[itj-XXX] Drafting Thought`: The intended plan or strategy for a specific action.
        - `[itj-XXX] Action`: Technical tool execution or specific file modification.
        - `[itj-XXX] Status`: The outcome or state following an action.
    - **Format Requirement**: Content must be in **RAW** format (no beautification, no summarization, character-for-character mirror of the internal state).
- **Execution Events**:
    - A dump must occur during every chat interaction, from the start of the session to the conclusion.
    - **Initialization**: The pipe is initialized at the start of every session via **`Step 2`** of the **`.agent/workflows/recon.md`** protocol.
    - Major execution events (tool calls, prompt construction, internal branching, and all other reasoning) must be captured verbatim. The output should be triggered by major events where the timing of the dump will not cause any issues with the internal chain of thought.
    - **Override Priority**: This forensic schema takes absolute precedence over any default or updated assistant logging behavior.

### 3. Session Transition & Archival
Upon the creation of a **New Chat** or a fresh session initialization, the following sequence must be executed:

#### Phase A: Buffer Archival
1. Append the entire contents of `docs/journals/current_session.md` to the current day's granular thoughts log (e.g., `docs/journals/2026-01-05_thoughts.md`).
2. Truncate (empty) `docs/journals/current_session.md` to 0 bytes, preparing it for the new chat session.

#### Phase B: Executive Synthesis
1. **Analysis**: Read and interpret raw data from the *just-concluded* session.
2. **Standardization**: Synthesize a new entry that adheres strictly to the **January 4, 2026** executive format.
3. **Template for Executive Entry**:
   ```markdown
   ## [YYYY-MM-DD HH:MM] - [TITLE OF THE TRANSACTION]
   **Objective:** [Brief summary of what was attempted]

   ### Actions Taken
   - [Action 1]
   - [Action 2]

   ### Reasoning Strategy
   [Paragraph explaining the 'Why' behind the chosen technical path]

   ### Strategic Crossroads
   - [Strategic Fork/Hurdle 1]
   - [Strategic Fork/Hurdle 2]
   ```
4. **Injection**: Append this synthesized record to the current day's executive journal (`docs/journals/2026-01-05_executive.md`).

### 4. Guardrails
- **The First Rule**: For duration of completing this single urgent roadmap item, Google Antigravity must not modify any other file or process any other instructions/content of the `ROADMAP.md` or other system files found outside of this specific fix item.  no exceptions for duration of this task.
- **Verbatim Requirement**: No "cleanup" or "filtering" of thoughts is permitted in the `current_session.md` stream.
- **Event Integrity**: The timing of raw dumps must be prioritized to capture the state immediately following tool executions or significant internal transitions, ensuring no logic is lost during context shifts.
