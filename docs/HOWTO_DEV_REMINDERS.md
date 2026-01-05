# Gravitas Grounded Research: Developer Capabilities & Reminders

This document outlines what **Antigravity** (the agent) and **Gravitas** (the research system) can do for you, alongside the specific "How-To" workflows for maximum productivity.

## 1. Automated Continuity (The Startup Methodology)
Every time a new session begins, the system automatically reconstructs the project state.
- **Strategic Crossroads First**: Every carryover MUST lead with unanswered strategic crossroads. These are the immediate hurdles and forks in the road for the project.
- **Deep Reconciliation**: Antigravity syncs with your latest strategic decisions in the `executive.md` journals.
- **Silent Metadata Sync**: A background machine-readable "vocabulary" is maintained to ensure the agent understands current protocols without manual configuration.
- **Context Resumption**: Resume complex research or coding tasks exactly where they left off, avoiding the "cold start" delay.

### Strategic Extraction Protocol
On each session, the agent extracts strategic reminders using the following methodology:
1.  **Scan Strategic Anchors**: Scans the most recent `executive.md` specifically seeking `## Strategic Decisions`, `🏁 STRATEGIC CROSSROADS`, and `## Current Objective`.
2.  **Filter for In-Progress State**: Identifies foundational naming changes, structural forks, and open todos that affect the project's current trajectory.
3.  **Synthesis vs. Redundancy**: Instead of duplicating raw logs, the agent synthesizes the current "project pulse" into today's carryover section.
4.  **Reasoning Isolation**: The granular `thoughts.md` track is intentionally isolated to keep context lean. While it serves as a critical audit trail for tool failures, its primary purpose is **Thinking Transparency**—allowing humans to reconstruct and understand the agent's internal reasoning process if needed.
5.  **Privacy Rule**: **IMPORTANT**: No agent should ever read a `thoughts.md` journal without a specific request from the USER.
6.  **Buffer-to-Archive Protocol**: To eliminate friction, active reasoning data is piped to `docs/journals/current_session.md` during the session. On every session start (Recon), the contents of this buffer are appended to the agent's daily **Reasoning Pipe** (`thoughts.md`) without modification, and the buffer is cleared.

## 2. Grounded Research & Journaling
- **Dual-Track Journaling**: We maintain a private audit trail in `docs/journals/`.
  - **Strategic History** (`executive.md`): Tracks major architecture, rebranding, and roadmap.
  - **Reasoning Pipes** (`thoughts.md` / `ReasoningPipe_{agentName}.md`): Captures "Drafting Thoughts" and action states. Primary purpose is providing humans a window into the agent's reasoning; secondary purpose is the foundation for **Phase 6 Self-Learning**.
- **Grounding Layers**: Direct access to federated documentation and vector memory.
- **Departmental Agents**: Specialized roles (Scout, Librarian, Archivist) handle distinct parts of the research lifecycle.

---

## 3. How-To: Updating Context for External AI
When working in an external chat (Gemini/OpenAI) without direct codebase access:
1. **Run Command**: Use the alias `UpdateContext`.
2. **Explore**: A Windows Explorer window will open to `GravitasNexusContext/Text`.
3. **Initialize**: Paste the content of **`Initial Context Prompt.md`** (the 1st message).
4. **Transfer**: Drag and drop all other documents from that folder into the chat once acknowledged.

---

## 4. Shared Shortcuts & Volume Control
### Terminal Aliases:
| Command | Action |
| :--- | :--- |
| `UpdateContext` | Refreshes external context files and opens Explorer. |
| `winE` | Opens Windows Explorer in the current WSL directory. |
| `reload` | Sources `~/.bashrc` to apply configuration changes. |
| `py` | Jumps to project root and activates the virtual environment. |
| `Gravitas` | Launches the Antigravity editor for the current directory. |

### Magic Words (Volume Control):
If the agent is logging too much, use these in the chat:
- **"scale back logging"**: Reduces the granularity of the logs.
- **"switch to Executive Only"**: Temporarily halts the Reasoning Pipe log.

---

## 5. Key Operational Rules
1. **Journal Visibility**: Journals are visible to agents and maintained for continuity. They are NOT included in `.gitignore` (as this blocks agent-writing tools), but are excluded from commits by policy.
2. **Selective Committing**: Agents responding to a "commit" directive MUST NOT include `docs/journals/` unless explicitly instructed by the user. 
   - **Agent Implementation**: Use `git add <files> :!docs/journals/` or explicitly list files while skipping the journals directory.
   - **Verification**: Always run `git status` (filtered) before committing to ensure journals are not staged.
3. **Journal Aging Policy**:
   - Current and Yesterday's journals are preserved for active context.
   - Journals older than **2 days** are strictly ignored/untracked.
   - Files older than **14 days** are purged by `./scripts/maintenance.py`.
4. **Git Status Filtering**: To view status without journal noise, use: `git status -- :!docs/journals/`

---

## 6. Self-Learning & Reasoning Pipes
To ensure **Bit-for-Bit Faithfulness** and eliminate **Cognitive Drift**, all granular thoughts and actions are recorded via a **Reasoning Pipe**. 
1. **The Reasoning Pipe Rule**: MANDATORY. Every task cycle MUST conclude with a verbatim dump of all internal reasoning/actions to the `current_session.md` buffer.
2. **Zero-Editing Policy**: The agent is strictly forbidden from summarizing, re-phrasing, or "cleaning up" internal processes for the pipe. The dump must be a character-for-character mirror of the internal reasoning or action state.
3. **The Observer Barrier**: Reasoning Pipes are for audit and self-learning only. Agents do not "read" their own session journals to maintain logic; they rely on the active context. This prevents recursion and memory pollution.
4. **Naming Convention**: Journals for departmental agents MUST follow the schema: `docs/journals/ReasoningPipe_{agentName}.md`.
5. **Startup Archive Sync**: Content from the previous session's buffer MUST be automatically appended to the correct Reasoning Pipe during the Recon workflow before the buffer is reset. (Telemetry database hits are managed separately in Phase 4.5).

---

## 7. Executive Journaling Standard (The 01-04 Pattern)
To maintain strategic continuity, all entries in `executive.md` must follow the "01-04 Pattern." This is the mandatory schema for high-level project management.
1. **Blueprint Reference**: Use the structure defined in `.agent/executive_template.md`.
2. **Action/Reasoning Split**: Always separate technical changes from architectural rationale.
3. **Strategic Crossroads**: Mandatory section for identifying forks/hurdles for human steering.
4. **No Status Reports**: Always favor strategy extraction over "done" lists.

---

## 8. Naming & Identity Protocols
To ensure the **Gravitas RAG** identifies context correctly, all documentation and chat interactions MUST maintain a strict firewall between the construction tool and the project being built.
1. **The Construction Tool**: The Google AI Assistant used by the developer is named **Antigravity**. Its custom logic is stored in `.agent/` and `ANTIGRAVITY_Scripts/`. References to "Antigravity" must ONLY refer to this external assistant.
2. **The Project/System**: The RAG system being built is named **Gravitas**. The internal orchestration, logic, and departmental specialists (e.g., **Gravitas Scout**, **Gravitas Librarian**) all belong to the **Gravitas** namespace. 
3. **Prohibited Terms**: The abbreviation **AGY** is a legacy project name and is strictly prohibited in current Gravitas documentation or code.
4. **Explicit Identification**: All agents and system components MUST be explicitly identified to ensure forensic clarity. Antigravity handles the orchestration of the development process; Gravitas handles the orchestration of the research platform.

---
9. **Table Visibility Override**: (MANDATORY) Due to a rendering bug where the **Antigravity** assistant fails to inherit dark/light theme colors for tables, all tabular data requests will be handled via:
   - **Persistent Storage**: A file will be generated in `/temporaryTesting/` with a date-stamped name (e.g., `2026-01-05_TableName.md`).
   - **Chat Notification**: The user will be notified of the file path and the reason for the side-channel delivery.
   - **Raw Code Fallback**: To ensure immediate visibility, the table's raw Markdown (non-interpreted) will be provided within a standard code block in the chat.

---
*Note: This file serves as the source of truth for the system's operational vocabulary. Maintaining this document ensures the agent remains aligned with human intent.*
