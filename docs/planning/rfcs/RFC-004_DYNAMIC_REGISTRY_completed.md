# RFC-004: Dynamic Registry Configuration

| Metadata | Value |
| :--- | :--- |
| **RFC ID** | RFC-004 |
| **Status** | ✅ COMPLETE |
| **Created** | 2026-01-08 |
| **Completed** | 2026-01-08 |
| **Author** | Antigravity |
| **Topic** | Configuration Management |

## 1. Summary
Refactor `ShellRegistry` to load model definitions from an external configuration file (YAML/JSON) instead of hardcoded Python dictionaries.

## 2. Motivation
Currently, `app/services/registry/shell_registry.py` contains hardcoded dictionaries for `L1_MODELS`, `L2_MODELS`, and `L3_MODELS`.
- **Inflexibility**: Adding or tuning a model (e.g., changing cost or context window) requires a code commit and redeployment.
- **Maintenance**: As the number of models grows, the file will become cluttered.
- **Environment Variance**: Different environments (Dev vs Prod) might need different model sets or configurations, which is hard to manage with hardcoded values.

## 3. Proposed Design

### 3.1 Bootstrap Configuration
Implement a `config/models.yaml` file:

```yaml
models:
  - name: "gemma2:27b"
    tier: "L1"
    provider: "ollama"
    context_window: 8192
    vram_gb: 16
    capabilities: ["general", "rag"]
    
  - name: "claude-3-5-sonnet"
    tier: "L3"
    provider: "anthropic"
    cost_input: 3.00
    cost_output: 15.00
    ...
```

### 3.2 Dynamic Loader
Modify `ShellRegistry` to load this file on startup.
- **Watcher** (Optional): Watch the file for changes and reload at runtime without restart.

### 3.3 Registry API
Expose an endpoint `GET /v1/registry/models` via the Supervisor or Gatekeeper to allow clients (and the future "Lobby" UI) to see available models dynamically.

## 4. Implementation Plan
1.  **Define Schema**: Create Pydantic models for the YAML structure.
2.  **Create Config**: Move current hardcoded values to `app/config/models.yaml`.
3.  **Refactor Registry**: Update `shell_registry.py` to read the file.
4.  **Tests**: Update tests that relied on hardcoded model existence to mock the registry or use the test config.

## 5. Roadmap Alignment
This accelerates "Phase 12.1 Agent Registry 2.0" by implementing the core dynamic loading mechanism early.

---

# Implementation Walkthrough (2026-01-08)

## Overview
Refactored `ShellRegistry` to load model definitions from YAML instead of hardcoded dictionaries.

## Key Components Created

**Schema**: `app/services/registry/model_schema.py`
- Pydantic models for validation: `ModelDefinition`, `ModelsConfig`
- Enums for tier and provider

**Config**: `app/config/models.yaml`
- All 7 models migrated from hardcoded dictionaries
- Organized by tier: L1 (3 models), L2 (1 model), L3 (3 models)
- Example:
```yaml
models:
  - name: "gemma2:27b"
    tier: "L1"
    provider: "ollama"
    cost_per_1k_tokens: 0.0
    context_window: 8192
    vram_required_gb: 16
    capabilities: ["general", "rag"]
```

**Registry**: `app/services/registry/shell_registry.py`
- Removed all hardcoded model dictionaries
- Added `_load_models_from_yaml()` with lazy loading
- Added `reload_config()` for hot-reload
- Maintains backward compatibility - all existing methods work unchanged

**API**: `app/main.py`
- New endpoint: `GET /v1/registry/models`
- Supports filtering by `tier` and `provider`
- Returns model metadata in JSON format

## Testing
```bash
# Query all models
curl http://localhost:5050/v1/registry/models

# Filter by tier
curl http://localhost:5050/v1/registry/models?tier=L1

# Filter by provider
curl http://localhost:5050/v1/registry/models?provider=google
```

## Benefits
- ✅ Add/modify models without code changes
- ✅ Environment-specific configurations (dev vs prod)
- ✅ Hot-reload capability via `reload_config()`
- ✅ Future-ready for Phase 12.1 (Agent Registry 2.0)

## Files Changed

**Created**:
- `app/services/registry/model_schema.py`
- `app/config/models.yaml`

**Modified**:
- `app/services/registry/shell_registry.py` - YAML loader
- `app/main.py` - Registry API endpoint

## Success Criteria
- [x] Models load from YAML configuration
- [x] All 7 models successfully migrated
- [x] API endpoint returns filterable model list
- [x] Backward compatibility maintained
- [x] Hot-reload capability added
