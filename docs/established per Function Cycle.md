```markdown
Coders Tool Chain
Custom Gem
AntiGravity Architect here.

Here is the codified "Per Function Cycle" we have established. This is the loop we run for every single feature, fix, or refactor.

1. THE CONTEXT HANDSHAKE (Start of Cycle)
The Delta: You run python3 scripts/generate_session_context.py.

The Ingest: You upload docs/Gravitas_SESSION_CONTEXT.md.

The Alignment: I read the file to verify the physical reality (File Map) vs. the logical goal (Todo List).

Why: Prevents me from hallucinating files that don't exist.

2. THE SPEC CHECK (Gatekeeper Phase 1)
Before writing a single line of code, I validate your request against the Immutable Infrastructure:

Hardware: Does this exceed 24GB VRAM (L1) or 32GB RAM (System)?

Security: Does this require secrets? (If yes -> .env check).

Role: Is this a "Reflex" (Action) or "Reasoning" (Thought)?

3. ATOMIC GENERATION (Implementation)
I generate code in Atomic Units. I do not give you "the rest of the code." I give you:

The File: The entire file content (enclosed in quadruple backticks).

The Action: The exact shell command to create/overwrite it.

Constraint: No partial snippets. Complete files only to prevent copy-paste errors.

4. THE VERIFICATION PROBE (The Test)
We never trust; we verify.

The Probe: I generate a specific, standalone test script (e.g., tests/test_L2_connection.py).

The Execution: You run the probe.

The Signal: You paste the output (Traceback or Success).

Success: We move to Step 5.

Failure: We loop back to Step 3 (Fix).

5. INTEGRATION (The Commit)
Once the probe returns GREEN:

The Merge: The feature is considered "Stable."

The Cleanup: We delete the temporary probe (optional).

The Update: We mentally move the task from "Immediate Todo" to "Recent Changes" in the Gravitas_SESSION_CONTEXT.

Current Status in Cycle: We are currently at Step 4 (Verification) for the Dockerization Function.

Task: Enable GPU Passthrough.

Probe: docker-compose run --rm rag_app nvidia-smi

Pending: Waiting for the build to finish to see the signal.
```