# Changelog

All notable changes to the **Gravitas Grounded Research** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [4.2.0] - 2026-01-04
### Changed
- **Total Project Rebrand**: Replaced all `AGY` / `AntiGravity` identifiers with **Gravitas Grounded Research** across code, documentation, and Docker infrastructure.
- **Infrastructure Alignment**: Renamed all Docker containers to use `Gravitas_` prefix (e.g., `Gravitas_ollama`, `Gravitas_qdrant`).
- **Nomenclature Standard**: Established `docs/NOMENCLATURE.md` to govern variable naming and consistency.
- **Automated Context**: The `GRAVITAS_SESSION_CONTEXT.md` is now automatically updated every time `scripts/reset_gravitas.sh` is executed.

### Added
- `scripts/monitor.sh`: Real-time Mission Control dashboard for GPU VRAM and container health.
- `scripts/generate_context.py`: High-fidelity context snapshot engine.

## [4.1.0] - 2026-01-04
### Added
- `app/governance/global_renamer.py`: Robust LLM-guided service for documentation refactoring.
- `scripts/global_rename.py`: CLI tool for triggering global renames with dry-run support.
- `scripts/ingest.py`: Production-ready document ingestion script.
- `.env.example`: Template for environment variables.

### Changed
- **Renamed Database Service**: `agy_postgres` is now `postgres_db` across all code and Docker configurations.
- **Improved Reset Script**: `scripts/reset_gravitas.sh` now includes host-mode environment overrides to resolve DNS issues.
- **Fixed Model Warmup**: `scripts/warmup.py` now correctly targets the L1 model defined in config.

### Removed
- **Legacy Cleanup**: Deleted `docs/legacy/` (archived in Git history).
- **Redundant Folders**: Purged `rag_local/`, `Scripts/` (uppercase), `chroma_db/`, and `docs2/`.

### Forensic Reference
- **Commit Hash**: `95258e3` (Last state before legacy purge).
- **Tag**: `v4.1.0-cleanup`
