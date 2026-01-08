# Gravitas Documentation

Welcome to the Gravitas documentation! This guide helps you navigate the organized documentation structure.

---

## 📖 Quick Start

- **New to Gravitas?** Start with [Master Overview](architecture/000_MASTER_OVERVIEW.md)
- **Setting up development?** See [Development Protocols](development/005_development_protocols.md) and [Coding Standards](development/CODING_STANDARDS.md)
- **Looking for API docs?** Check [Model Governance](architecture/007_model_governance.md) and [Reasoning Pipes](architecture/008_reasoning_pipes.md)
- **Need help?** See [FAQ](reference/FAQ.md)

---

## 📂 Documentation Structure

### 🏛️ [architecture/](architecture/)
Core system design and architecture documents

| Document | Description |
|----------|-------------|
| [000_MASTER_OVERVIEW.md](architecture/000_MASTER_OVERVIEW.md) | **Start here** - System overview |
| [001_core_architecture.md](architecture/001_core_architecture.md) | Core architectural patterns |
| [002_vector_memory.md](architecture/002_vector_memory.md) | Vector memory system |
| [003_security_gatekeeper.md](architecture/003_security_gatekeeper.md) | Security & access control |
| [004_hardware_operations.md](architecture/004_hardware_operations.md) | GPU & hardware management |
| [007_model_governance.md](architecture/007_model_governance.md) | L1/L2/L3 routing & model governance |
| [008_reasoning_pipes.md](architecture/008_reasoning_pipes.md) | Reasoning pipe protocol |
| [009_access_control.md](architecture/009_access_control.md) | Access control policies |
| [GRAVITAS_NOMENCLATURE.md](architecture/GRAVITAS_NOMENCLATURE.md) | System terminology |

---

### 👨‍💻 [development/](development/)
Development guides, protocols, and standards

| Document | Description |
|----------|-------------|
| [005_development_protocols.md](development/005_development_protocols.md) | **Core dev protocols** - TDD, SOLID, version control |
| [CODING_STANDARDS.md](development/CODING_STANDARDS.md) | **Coding standards** - Datetime handling, error handling, type hints |
| [006_TELEMETRY_CALIBRATION.md](development/006_TELEMETRY_CALIBRATION.md) | Telemetry & performance monitoring |
| [TESTING_GUIDE.md](development/TESTING_GUIDE.md) | Testing guidelines |
| [WRAPPER_DEVELOPMENT_GUIDE.md](development/WRAPPER_DEVELOPMENT_GUIDE.md) | Agent wrapper development |
| [HOWTO_DEV_REMINDERS.md](development/HOWTO_DEV_REMINDERS.md) | Quick dev tips |
| [GOOGLE_ANTIGRAVITY_SPEC.md](development/GOOGLE_ANTIGRAVITY_SPEC.md) | Antigravity assistant spec |
| [hardware_rig.md](development/hardware_rig.md) | Hardware setup guide |

---

### 📋 [rfcs/](rfcs/)
Request for Comments - Architectural proposals

| RFC | Description | Status |
|-----|-------------|--------|
| [RFC-001-SupervisorDecomposition.md](rfcs/RFC-001-SupervisorDecomposition.md) | Decompose Supervisor into microservices | ✅ Phase 1 Complete |
| [CurrentDockerArchitectureAnalysis.md](rfcs/CurrentDockerArchitectureAnalysis.md) | Docker independence analysis | Reference |

---

### 🚨 [incidents/](incidents/)
Incident reports and postmortems

| Document | Description |
|----------|-------------|
| [INCIDENT_LOG.md](incidents/INCIDENT_LOG.md) | **Active incident log** |
| [criticalSupervisorFailureReport.md](incidents/criticalSupervisorFailureReport.md) | INC-2026-001: Supervisor dependency failure |
| [todoSupervisorDebugV2.md](incidents/todoSupervisorDebugV2.md) | Supervisor debug plan (resolved) |
| [archived/](incidents/archived/) | Historical incident logs |

---

### ✅ [phases/](phases/)
Phase completion summaries and documentation

| Phase | Status | Documents |
|-------|--------|-----------|
| **Phase 4.5** | ✅ Complete | [Completion Summary](phases/Phase_4.5/PHASE_4.5_COMPLETION_SUMMARY.md) |
| **Phase 5** | ✅ Complete | [Final Summary](phases/Phase_5/PHASE_5_FINAL_COMPLETION_SUMMARY.md) |
| **Phase 6** | ✅ Complete | [Value Doc](phases/Phase_6/Phase_6_Value.md), [TODO folders](phases/Phase_6/todo/) |
| **Phase 7** | 🚧 In Progress | [TODO7.md](phases/Phase_7/TODO7.md) |
| **RFC-001 Phase 1** | ✅ Complete | [Guardian Extraction](phases/Phase_RFC001/Phase1_Guardian_Extraction_Complete.md) |

---

### 🗺️ [planning/](planning/)
Roadmaps and strategic planning

| Document | Description |
|----------|-------------|
| [ROADMAP.md](planning/ROADMAP.md) | **Current roadmap** |
| [ROADMAP_COMPLETION_CRITERIA_UPDATE.md](planning/ROADMAP_COMPLETION_CRITERIA_UPDATE.md) | Completion criteria |
| [STRATEGY_SESSION_2026_01_04.md](planning/STRATEGY_SESSION_2026_01_04.md) | Strategy session notes |

---

### 📚 [reference/](reference/)
Reference guides and context documents

| Document | Description |
|----------|-------------|
| [FAQ.md](reference/FAQ.md) | Frequently asked questions |
| [GRAVITAS_SESSION_CONTEXT.md](reference/GRAVITAS_SESSION_CONTEXT.md) | Session context & history |
| [model_integration.md](reference/model_integration.md) | Model integration guide |
| [gemini_3_model_guide.md](reference/gemini_3_model_guide.md) | Gemini 3.0 guide |
| [function_cycles.md](reference/function_cycles.md) | Function lifecycle docs |
| [BACKUP_SETUP.md](reference/BACKUP_SETUP.md) | Backup configuration |
| [concepts/](reference/concepts/) | Conceptual documentation |

---

### 📝 [sessions/](sessions/)
Session summaries and handover documents

| Document | Description |
|----------|-------------|
| [COMPLETE_SESSION_SUMMARY.md](sessions/COMPLETE_SESSION_SUMMARY.md) | Session completion summary |
| [SESSION_COMPLETE_SUMMARY.md](sessions/SESSION_COMPLETE_SUMMARY.md) | Another session summary |
| [SESSION_SUMMARY_RAG_TESTING.md](sessions/SESSION_SUMMARY_RAG_TESTING.md) | RAG testing session |
| [Initial Context Prompt.md](sessions/Initial%20Context%20Prompt.md) | Initial context |
| [handovers/](sessions/handovers/) | Session handover documents |

---

### 🧪 [testing/](testing/)
Testing guides and results

| Document | Description |
|----------|-------------|
| [TEST_GUIDE.md](testing/TEST_GUIDE.md) | Testing guidelines |
| [TEST_AUDIT.md](testing/TEST_AUDIT.md) | Test audit results |
| [TEST_AUDIT_SUMMARY.md](testing/TEST_AUDIT_SUMMARY.md) | Audit summary |
| [TEST_RESULTS_INTEGRATED_RAG.md](testing/TEST_RESULTS_INTEGRATED_RAG.md) | RAG integration test results |
| [TELEMETRY_INTEGRATION_TEST_RESULTS.md](testing/TELEMETRY_INTEGRATION_TEST_RESULTS.md) | Telemetry test results |
| [SPECIFICATION_TESTING_SUMMARY.md](testing/SPECIFICATION_TESTING_SUMMARY.md) | Spec testing summary |

---

### 🐛 [debug/](debug/)
Debugging guides and resolution documents

| Document | Description |
|----------|-------------|
| [RAG_DEBUG_ANALYSIS.md](debug/RAG_DEBUG_ANALYSIS.md) | RAG debugging analysis |
| [RAG_REFUSAL_RESOLUTION.md](debug/RAG_REFUSAL_RESOLUTION.md) | RAG refusal fix |
| [RESET_SCRIPT_UPDATE.md](debug/RESET_SCRIPT_UPDATE.md) | Reset script improvements |
| [NEXUS_RESCAN_IMPROVEMENTS.md](debug/NEXUS_RESCAN_IMPROVEMENTS.md) | Nexus rescan fixes |

---

### 📓 [journals/](journals/)
Reasoning pipe journals and agent logs (auto-generated)

Contains timestamped journal files from agent reasoning pipes.

---

### 🗄️ [archived/](archived/)
Deprecated or historical documentation

Old documentation kept for reference.

---

## 🔍 Finding What You Need

### By Role

**Developers:**
1. Start: [Development Protocols](development/005_development_protocols.md)
2. Then: [Coding Standards](development/CODING_STANDARDS.md)
3. Reference: [Testing Guide](development/TESTING_GUIDE.md)

**Architects:**
1. Start: [Master Overview](architecture/000_MASTER_OVERVIEW.md)
2. Then: [Core Architecture](architecture/001_core_architecture.md)
3. Reference: [RFCs](rfcs/)

**Operators:**
1. Start: [Hardware Operations](architecture/004_hardware_operations.md)
2. Then: [Incident Log](incidents/INCIDENT_LOG.md)
3. Reference: [Backup Setup](reference/BACKUP_SETUP.md)

### By Task

- **Adding a new model?** → [Model Governance](architecture/007_model_governance.md)
- **Creating an agent?** → [Wrapper Development Guide](development/WRAPPER_DEVELOPMENT_GUIDE.md)
- **Debugging an issue?** → [Debug Docs](debug/) + [Incident Log](incidents/INCIDENT_LOG.md)
- **Understanding routing?** → [Model Governance: L1/L2/L3](architecture/007_model_governance.md)
- **Setting up auth?** → [Access Control](architecture/009_access_control.md)

---

## 📊 Documentation Stats

- **Total Categories**: 10 organized directories
- **Architecture Docs**: 9 files
- **Development Guides**: 8 files
- **Phase Completions**: 5 phases documented
- **Active RFCs**: 1 (RFC-001)
- **Last Updated**: 2026-01-07

---

## 🤝 Contributing

When adding new documentation:
1. Place in appropriate category directory
2. Follow naming conventions (e.g., `NNN_descriptive_name.md` for core docs)
3. Update this README if adding new categories
4. Reference from [Development Protocols](development/005_development_protocols.md) if establishing new standards

---

**Questions?** See [FAQ](reference/FAQ.md) or check [Gravitas Session Context](reference/GRAVITAS_SESSION_CONTEXT.md)
