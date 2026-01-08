# Ghost/Shell Quick Reference Card

## What Changed in Phase 6.5?

### Before (Phase 6.0)
```python
# Agent and Model were conflated
agent_name = "gemma2:27b"  # Is this an agent or a model?
```

### After (Phase 6.5)
```python
# Clear separation
ghost_name = "Librarian"    # WHO (agent identity/role)
shell_id = "gemma2:27b"     # HOW (execution model)
```

---

## Quick Translation Guide

| Old Concept | New Concept | Example |
|-------------|-------------|---------|
| Agent | Ghost + Shell | "Librarian" (Ghost) using "gemma2:27b" (Shell) |
| Model | Shell | "gemini-1.5-pro" is a Shell |
| Agent Identity | Ghost | "Scout", "Librarian", "Supervisor" |
| AgentRegistry | ShellRegistry | Catalog of available models |
| N/A | GhostRegistry | Catalog of agent roles |

---

## Import Cheat Sheet

### OLD WAY (Deprecated, but still works)
```python
from app.services.registry.agent_registry import AgentRegistry

# Warning: AgentRegistry is deprecated!
model = AgentRegistry.get_model("gemma2:27b")
```

### NEW WAY (Recommended)
```python
from app.services.registry.ghost_registry import GhostRegistry
from app.services.registry.shell_registry import ShellRegistry

# Get agent identity
ghost = GhostRegistry.get_ghost("Librarian")
# Returns: GhostSpec(name="Librarian", preferred_shell="gemma2:27b", ...)

# Get model specification  
shell = ShellRegistry.get_model("gemma2:27b")
# Returns: ModelSpec(name="gemma2:27b", tier=L1, cost=0.0, ...)
```

---

## Code Migration Examples

### 1. ReasoningPipe Initialization

**Before:**
```python
pipe = ReasoningPipe(
    agent_name="gemma2:27b",  # Confusing: is this the agent or model?
    session_id="abc123",
    model="gemma2:27b",       # Duplicate info
    tier="L1"
)
```

**After:**
```python
pipe = ReasoningPipe(
    ghost_name="Librarian",   # Clear: this is the agent identity
    session_id="abc123",
    model="gemma2:27b",       # This is the execution model
    tier="L1"
)
```

**Backward Compatible (still works):**
```python
pipe = ReasoningPipe(
    agent_name="Librarian",   # Automatically maps to ghost_name
    session_id="abc123",
    model="gemma2:27b",
    tier="L1"
)
```

### 2. Database Saves

**Before:**
```python
await db.save_history(
    role="assistant",
    content="Response text"
)
# Lost: which agent and which model?
```

**After:**
```python
await db.save_history(
    role="assistant",
    content="Response text",
    ghost_id="Librarian",      # Who performed this action
    shell_id="gemma2:27b"      # How it was executed
)
```

**Backward Compatible (uses defaults):**
```python
await db.save_history(
    role="assistant",
    content="Response text"
    # ghost_id defaults to "unknown_ghost"
    # shell_id defaults to "unknown_shell"
)
```

### 3. Reading History

**Before:**
```python
history = await db.get_recent_history(limit=5)
# Returns: [{"role": "user", "content": "..."}]
```

**After:**
```python
history = await db.get_recent_history(limit=5)
# Returns: [{"role": "user", "content": "...", "ghost_id": "Librarian", "shell_id": "gemma2:27b"}]
```

---

## Journal File Naming

### Before
```
docs/journals/ReasoningPipe_gemma2:27b_2026-01-06.md
docs/journals/ReasoningPipe_gemma2:27b.md (summary)
```

### After
```
docs/journals/Librarian_2026-01-06.md
docs/journals/Librarian_journal.md (summary)
```

**Benefit**: When you upgrade from gemma2:27b → llama3:70b, the Librarian's journal stays continuous!

---

## Common Patterns

### Pattern: Get Ghost's Preferred Shell
```python
from app.services.registry.ghost_registry import GhostRegistry
from app.services.registry.shell_registry import ShellRegistry

# Get the Ghost
ghost = GhostRegistry.get_ghost("Librarian")

# Get its preferred Shell
shell = ShellRegistry.get_model(ghost.preferred_shell)

print(f"{ghost.name} prefers {shell.name} ({shell.tier})")
# Output: "Librarian prefers gemma2:27b (L1)"
```

### Pattern: Find Ghost for a Capability
```python
from app.services.registry.ghost_registry import GhostRegistry

# Who can do web searches?
ghost = GhostRegistry.get_ghost_for_capability("web_search")
print(ghost.name)  # "Scout"
```

### Pattern: Find Cheapest Shell for RAG
```python
from app.services.registry.shell_registry import ShellRegistry, ModelCapability

shell = ShellRegistry.get_cheapest_model_for_capability(ModelCapability.RAG)
print(f"{shell.name}: ${shell.cost_per_1k_tokens}/1k tokens")
# "gemma2:27b: $0.0/1k tokens"
```

---

## Mental Model

Think of it like an office:

```
Ghost = The Employee (permanent role)
├─ Name: "Librarian"
├─ Role: Indexer
├─ Responsibilities: Document processing, chunking, embedding
├─ Capabilities: [RAG, summarization, indexing]
└─ Uses (Shell): "gemma2:27b"

Shell = The Computer They Use (swappable tool)
├─ Model: "gemma2:27b"
├─ Tier: L1 (Local)
├─ VRAM: 16GB
├─ Cost: $0.00/1k tokens
└─ Specs: 8K context, 150ms latency
```

**If the Librarian gets a new computer (Shell upgrade):**
- ✅ Their role stays the same (Ghost persists)
- ✅ Their journals stay organized under "Librarian"
- ✅ Historical cost tracking shows "Librarian cost over time"
- ✅ We can compare: "Was Librarian faster with Gemma or Llama?"

**If we hire a new employee (Ghost activation):**
- ✅ New Ghost in GhostRegistry: "Miner"
- ✅ Assign preferred Shell: "gemini-1.5-pro"
- ✅ Define capabilities: ["video_download", "transcription"]
- ✅ Start tracking their work separately

---

## Migration Checklist

When updating your agent code:

- [ ] Change `agent_name` → `ghost_name` in ReasoningPipe
- [ ] Add `ghost_id` and `shell_id` to database saves
- [ ] Import from `ghost_registry` for identities
- [ ] Import from `shell_registry` for models
- [ ] Update docstrings to use Ghost/Shell terminology
- [ ] Test that journals appear in `docs/journals/{GhostName}_*.md`
- [ ] Verify database entries have ghost_id/shell_id populated

---

## FAQ

**Q: Do I have to update my code immediately?**  
A: No. Backward compatibility is maintained. You'll see deprecation warnings, but everything works.

**Q: When should I migrate?**  
A: Before Phase 7 (Security Tier). Deprecation layer will be removed then.

**Q: What happens to old journal files?**  
A: They stay as-is. New journals use the new naming scheme.

**Q: What happens to old database records?**  
A: They have ghost_id="legacy_ghost" and shell_id="legacy_shell". New records use proper IDs.

**Q: Can I still import AgentRegistry?**  
A: Yes, but you'll get a deprecation warning. Use ShellRegistry directly.

**Q: How do I add a new Ghost?**  
A: Add to `PLANNED_GHOSTS` in `ghost_registry.py`, then call `GhostRegistry.activate_ghost(name)`.

**Q: How do I add a new Shell?**  
A: Add to `L1_MODELS`, `L2_MODELS`, or `L3_MODELS` in `shell_registry.py`.

---

## Need Help?

- **Architecture review**: `docs/handovers/2026-01-06_Conceptual_Review_Response.md`
- **Execution summary**: `docs/Phase_6.5_TODO/EXECUTION_SUMMARY.md`
- **Step-by-step log**: `docs/Phase_6.5_TODO/PROGRESS.md`
- **Examples**: This file!

---

**Remember**: Ghost = WHO, Shell = HOW. Keep them separate, and your architecture stays clean! 🎭🐚
