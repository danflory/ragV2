---
description: Manually trigger high-fidelity cognitive mirroring of the current state.
---

// turbo
1. **Reconstruct Cognitive Trace**: Synthesize your current turn's Internal Monologue and Actions into a high-fidelity Markdown block.
2. **Execute reasoning_pipe**: 
   ```bash
   echo "<thought_tap>\nInternal Monologue: [Your Thoughts]\nAction: [Your Tools]\n</thought_tap>" | python3 ANTIGRAVITY_Scripts/reasoning_pipe.py --stdin
   ```
3. **Verify Compliance**: Ensure the entry is appended to `docs/journals/current_session.md` with a valid `[itj-XXX]` ID.
