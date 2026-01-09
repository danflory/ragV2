---
description: Run the Antigravity Reasoning Pipe to handle session transitions and archival. 
---

> [!IMPORTANT]
> **Proactive Requirement**: As an agent, I must execute this synthesis workflow automatically at the conclusion of every major project milestone (e.g., feature verification, phase completion) without being explicitly prompted.

1. **Executive Synthesis**: 
   - Read the current session buffer (`docs/journals/thoughts/current_session.md`) and today's high-fidelity thoughts.
   - Synthesize the technical details into a high-level executive summary following the **1/04 format**:
     - **Objective**: Current primary goal.
     - **Actions Taken**: Bulleted summary of technical accomplishments.
     - **Reasoning Strategy**: Detailed paragraph on the "Why" and architectural rationale.
     - **Strategic Crossroads**: Open issues, design choices, or risks to consider.
   - Append this synthesis to today's executive journal (`docs/journals/executive/YYYY-MM-DD_executive.md`).

2. **Execute Reasoning Pipe & Sync**: 
   ```bash
   python3 scripts/crossroads_tracker.py --sync && \
   python3 scripts/crossroads_tracker.py --status && \
   python3 ANTIGRAVITY_Scripts/reasoning_pipe.py --init
   ```
   *Note: This synchronizes strategic crossroads to the local SQLite tool before clearing the session buffer.*
