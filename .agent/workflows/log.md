---
description: Manually trigger high-fidelity cognitive mirroring of the current state.
---

// turbo
1. **Reconstruct Cognitive Trace**: Capture the **full depth** of your internal reasoning (equivalent to the 'thought for Xs' UI block). Do not summarize; include architectural trade-offs, syntax verifications, and diagnostic pathways.
2. **Execute reasoning_pipe**: 
   ```bash
   echo "### Deep-Dive Reasoning: [Current Focus]\n\n[Full-resolution internal monologue...]" | python3 ANTIGRAVITY_Scripts/reasoning_pipe.py --stdin
   ```
3. **Verify Compliance**: Ensure the entry mirrors the actual complexity of the AI's internal processing.
