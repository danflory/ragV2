# Incident & Recovery Log: 2026-01-07
**Subject**: Docker Restoration, BorgBackup Implementation, and Architectural Refactor

## 1. Incident Overview
Following a Docker Desktop clean reinstallation on Windows 10, the Gravitas environment required a full restoration of services, data verification, and a robust backup strategy to prevent data loss (specifically the ~26GB of model files).

---

## 2. Bug: The "Ghost Container" Conflict
**Symptoms**: 
- `docker-compose up` failed with: `Error response from daemon: Conflict. The container name "/Gravitas_lobby" is already in use by container [ID].`
- `docker ps -a` showed no such container.
- `docker rm -f [ID]` returned `No such container`.
- `docker inspect` returned `No such object`.

**Root Cause**: A "zombie" entry in the Docker engine's name registry. This often occurs during a hard Docker Desktop reset or WSL filesystem sync error where the metadata persists but the container object is gone.

**Resolution (Workaround)**: 
Renamed the container in `docker-compose.yml` from `Gravitas_lobby` to `Gravitas_lobby_v2`. This bypassed the name registry conflict immediately without requiring another full Docker engine reset.

---

## 3. Structural Change: Independent Services
**Change**: Removed all `depends_on` blocks from `docker-compose.yml`.

**Rationale (Priority 1 Implementation)**: 
Previously, `docker-compose` enforced a rigid startup order. If the `mcp` image was rebuilding (taking 15+ minutes), it would block `ollama` and `postgres` from starting, even though they were ready.
- **New Behavior**: All 8 services now start independently and concurrently.
- **Benefit**: If one service crashes or needs a long rebuild, the "Big Players" (Ollama, Vector DB, Postgres) remain accessible and functional. The application logic is now responsible for handling service connection retries rather than Docker enforcing a block.

---

## 4. Setup: BorgBackup (WSL vs. Windows)
**Decision**: Migrated from PowerShell-based BorgBackup to **WSL (Ubuntu) native BorgBackup**.

**Rationale**: 
- The Windows version of BorgBackup is currently flagged as experimental/unstable by the official project.
- Since Gravitas data resides inside the WSL filesystem (`ext4.vhdx`), running Borg natively in Linux avoids cross-OS filesystem metadata errors and performance overhead.
- **Performance**: The initial backup of 51.27 GB was deduplicated down to **32.56 GB** (saving ~19GB) in 12 minutes.

**Configured Scripts**:
- `scripts/setup_backup.sh`: One-time setup and repo initialization.
- `scripts/backup_now.sh`: Manual incremental backup.
- `scripts/list_backups.sh`: List archive history.
- `scripts/restore_backup.sh`: Extraction utility.

---

## 5. Data Verification
- **Primary Compute (C:)**: Confirmed Gravitas and Docker Data live on the M.2 NVMe C: drive for maximum inference speed (loading 18GB models in <10s vs 60s+ on the old drive).
- **Secondary Storage (D:)**: Identified as a slower secondary drive, kept available for expansion but bypassed for performance-critical AI models.
- **Backup (F:)**: 10TB drive confirmed as the destination for BorgBackup repositories.

---

## 6. Permissions Found & Fixed
**Issue**: Ollama service reported "No models found" despite 22GB being present in the data folder.
**Cause**: Permission mismatch after Docker/WSL reinstallation. Container `root` user couldn't read host files owned by previous user IDs.
**Fix**:
```bash
sudo chown -R $USER:$USER ./data/ollama_models
chmod -R 775 ./data/ollama_models
```

---

## 7. Current System State
- **Services**: All 8 independent services confirmed **Running**.
- **Model Brains**: `gemma2:27b`, `codellama:13b`, and `codellama:7b` confirmed **Online** and mapped.
- **Backup**: First full archive successfully stored and encrypted on F: drive.

---
**Documented by Antigravity AI**  
*Ref: Priority 1 - Independent Service Architecture*
