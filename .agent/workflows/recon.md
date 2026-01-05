---
description: Fast-start reconnaissance to sync with the dual-track journaling system and current project state.
---

// turbo-all
1. Run \`python3 /home/dflory/dev_env/rag_local/scripts/sync_vocabulary.py\` to ensure the machine-readable vocabulary is up-to-date.
2. Load and honor **\`.agent/vocabulary.md\`**.
3. Identify today's journal files in **\`docs/journals/\`**. If missing, initialize them.
4. Read the last 50 lines of the most recent **\`executive.md\`** for strategic carryover.
4. Verify current development **"Phase"** by listing the root directory for recent `todo*.md` or `ROADMAP.md`.
5. Start current session journaling with a **"Recon Complete"** entry in today's **`thoughts.md`**.
6. Report current trajectory to the user.
