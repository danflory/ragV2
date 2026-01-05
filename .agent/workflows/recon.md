---
description: Fast-start reconnaissance to sync with the dual-track journaling system and current project state.
---

// turbo-all
1. Run \`python3 /home/dflory/dev_env/rag_local/scripts/sync_vocabulary.py\` to ensure the machine-readable vocabulary is up-to-date.
2. Load and honor **\`.agent/vocabulary.md\`**.
3. Identify today's journal files in **`docs/journals/`**. If missing, initialize them.
4. **Buffer-to-Archive Sync**: If `docs/journals/current_session.md` exists and is not empty, append its contents to the most recent daily **Reasoning Pipe** (`thoughts.md`) and then clear `current_session.md`.
5. Read the last 50 lines of the most recent **`executive.md`** for strategic carryover.
6. Verify current development **"Phase"** by checking for recent `todo*.md` or **`ROADMAP.md`**.
7. Start current session journaling with a **"Recon Complete"** entry in **`current_session.md`**.
8. Report current trajectory to the user.
9. **Verify Infrastructure**: Confirm existence of **`.agent/executive_template.md`** and **`ANTIGRAVITY_Scripts/reasoning_pipe.py`**.
10. **Enforce Reasoning Pipe**: All subsequent turns must conclude with a verbatim character-for-character dump to `current_session.md` as per **Section 6 of `HOWTO_DEV_REMINDERS.md`**.
