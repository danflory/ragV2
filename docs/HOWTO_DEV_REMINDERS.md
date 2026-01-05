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
4.  **Forensic Isolation**: The granular `thoughts.md` track is intentionally isolated to keep context lean. While it serves as a critical audit trail for tool failures, its primary purpose is **Thinking Transparency**—allowing humans to reconstruct and understand the agent's internal reasoning process if needed.
5.  **Privacy Rule**: **IMPORTANT**: No agent should ever read a `thoughts.md` journal without a specific request from the USER.

## 2. Grounded Research & Journaling
- **Dual-Track Journaling**: We maintain a private audit trail in `docs/journals/`.
  - **Strategic History** (`executive.md`): Tracks major architecture, rebranding, and roadmap.
  - **Forensic Logs** (`thoughts.md`): Captures "Drafting Thoughts" and tool details. Primary purpose is providing humans a window into the agent's step-by-step reasoning; secondary purpose is forensic auditing for model errors.
- **Grounding Layers**: Direct access to federated documentation and vector memory.
- **Departmental Agents**: Specialized roles (Scout, Librarian, Archivist) handle distinct parts of the research lifecycle.

---

## 3. How-To: Updating Context for External AI
When working in an external chat (Gemini/OpenAI) without direct codebase access:
1. **Run Command**: Use the alias `UpdateContext`.
2. **Explore**: A Windows Explorer window will open to `AntiGravityNexusContext/Text`.
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
- **"switch to Executive Only"**: Temporarily halts the `thoughts.md` log.

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
*Note: This file serves as the source of truth for the system's operational vocabulary. Maintaining this document ensures the agent remains aligned with human intent.*
