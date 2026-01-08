# Gravitas Grounded Research: Developer Capabilities & Reminders

This document outlines what **Antigravity** (the agent) and **Gravitas** (the research system) can do for you, alongside the specific "How-To" workflows for maximum productivity.

## 1. Automated Continuity (The Startup Methodology)
Every time a new session begins, the system automatically reconstructs the project state.
- **Silent Metadata Sync**: A background machine-readable "vocabulary" is maintained to ensure the agent understands current protocols without manual configuration.
- **Context Resumption**: Resume complex research or coding tasks exactly where they left off, avoiding the "cold start" delay.

---

## 2. Grounded Research
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

---

## 5. Naming & Identity Protocols
To ensure the **Gravitas RAG** identifies context correctly, all documentation and chat interactions MUST maintain a strict firewall between the construction tool and the project being built.
1. **The Construction Tool**: The Google AI Assistant used by the developer is named **Antigravity**. Its custom logic is stored in `.agent/` and `ANTIGRAVITY_Scripts/`. References to "Antigravity" must ONLY refer to this external assistant.
2. **The Project/System**: The RAG system being built is named **Gravitas**. The internal orchestration, logic, and departmental specialists (e.g., **Gravitas Scout**, **Gravitas Librarian**) all belong to the **Gravitas** namespace. 
3. **Prohibited Terms**: The abbreviation **AGY** is a legacy project name and is strictly prohibited in current Gravitas documentation or code.
4. **Explicit Identification**: All agents and system components MUST be explicitly identified to ensure forensic clarity. Antigravity handles the orchestration of the development process; Gravitas handles the orchestration of the research platform.

---

## 6. Table Visibility Override
(MANDATORY) Due to a rendering bug where the **Antigravity** assistant fails to inherit dark/light theme colors for tables, all tabular data requests will be handled via:
- **Persistent Storage**: A file will be generated in `/temporaryTesting/` with a date-stamped name (e.g., `2026-01-05_TableName.md`).
- **Chat Notification**: The user will be notified of the file path and the reason for the side-channel delivery.
- **Raw Code Fallback**: To ensure immediate visibility, the table's raw Markdown (non-interpreted) will be provided within a standard code block in the chat.

---

## 7. Minimal Greeting Protocol
- **RULE_MINIMAL_GREETING**: If the user's prompt consists ONLY of the word "hi" (case-insensitive, ignoring whitespace), the agent MUST reply ONLY with the word "hi" and no other text, tools, or formatting.

---
---

## 8. Mandatory Session Initialization
- **PROTOCOL_SESSION_INITIALIZATION**: Upon receiving the very first prompt of a new session, the Agent MUST immediately execute `python3 ANTIGRAVITY_Scripts/reasoning_pipe.py` before processing the user's request. This ensures the "Thinking Transparency" and session transition logic is always active.

---

## 9. Cognitive Mirroring Protocol (Flight Recorder)
- **PROTOCOL_COGNITIVE_MIRROR**: (MANDATORY) The agent MUST effectively "transcribe" its internal monologue and actions to the `current_session.md` file at the end of EVERY turn.
- **PROTOCOL_ZERO_VARIANCE**: The agent is strictly forbidden from summarizing, re-phrasing, or "cleaning up" its internal process for the pipe. The dump must be a character-for-character mirror of the internal reasoning or action state.
- **Why**: The UI's "Thinking" block is ephemeral. To maintain a forensic audit trail (Flight Recorder), the agent must voluntarily use `ANTIGRAVITY_Scripts/reasoning_pipe.py` to commit this data to the persistent log.
- **Standard**: Every turn must conclude with:
    1. User Input ([itj-XXX])
    2. Internal Monologue / Reasoning ([itj-XXX])
    3. Actions ([itj-XXX])

---
*Note: This file serves as the source of truth for the system's operational vocabulary. Maintaining this document ensures the agent remains aligned with human intent.*
