# Gravitas Backup Setup with BorgBackup + Vorta

**Last Updated**: 2026-01-07  
**Backup Location**: `F:\dockerDesktopFromBorgeBackup\`

## Quick Start

### 1. Installation

```powershell
# Install BorgBackup + Vorta using winget
winget install BorgBackup.BorgBackup
winget install Vorta.Vorta
```

**Alternative Manual Install:**
- BorgBackup: https://github.com/borgbackup/borg/releases/latest
- Vorta: https://github.com/borgbase/vorta/releases/latest

---

## 2. Initialize Repository (One-Time Setup)

```powershell
# Create backup directory
New-Item -ItemType Directory -Path "F:\dockerDesktopFromBorgeBackup" -Force

# Initialize encrypted repository
borg init --encryption=repokey F:\dockerDesktopFromBorgeBackup
```

**⚠️ CRITICAL**: You will be prompted for a passphrase. 
- Choose a strong passphrase
- **WRITE IT DOWN** - Without it, backups are UNRECOVERABLE
- Store passphrase in password manager or secure location

**Recommended Passphrase Format**: `Gravitas-Backup-2026-SecurePhrase!`

---

## 3. What Gets Backed Up

### ✅ Included:
```
D:\dev_env\Gravitas\
├── app/                    ← All Python code
├── tests/                  ← Test suites
├── docs/                   ← Documentation
├── data/
│   ├── ollama_models/      ← **CRITICAL** - Model files (15GB+)
│   ├── qdrant/             ← Vector database
│   ├── postgres_data/      ← Chat history
│   └── model_backup/       ← Model backups
├── docker-compose.yml      ← Infrastructure config
├── requirements.txt        ← Dependencies
├── .env                    ← Environment variables
└── README.md
```

### ❌ Excluded:
```
- venv/                     ← Recreate with pip install
- __pycache__/              ← Generated files
- *.pyc                     ← Compiled Python
- .git/                     ← Use GitHub instead
- node_modules/             ← Recreate with npm install
- data/minio/               ← Usually regenerable
```

---

## 4. Manual Backup Commands

### Create Backup
```powershell
# Full backup with progress
borg create --stats --progress `
  --exclude '**/venv' `
  --exclude '**/__pycache__' `
  --exclude '**/*.pyc' `
  --exclude '.git' `
  --exclude '**/node_modules' `
  F:\dockerDesktopFromBorgeBackup::"{now:%Y-%m-%d_%H-%M-%S}" `
  D:\dev_env\Gravitas
```

### List All Backups
```powershell
borg list F:\dockerDesktopFromBorgeBackup
```

### Show Backup Details
```powershell
# Info about specific backup
borg info F:\dockerDesktopFromBorgeBackup::2026-01-07_13-00-00

# Info about latest backup
borg info F:\dockerDesktopFromBorgeBackup::
```

### Restore Entire Backup
```powershell
# Extract to new location
borg extract F:\dockerDesktopFromBorgeBackup::2026-01-07_13-00-00 `
  --target D:\dev_env\Gravitas-RESTORED
```

### Restore Specific Files/Folders
```powershell
# Restore just the models
borg extract F:\dockerDesktopFromBorgeBackup::2026-01-07_13-00-00 `
  data/ollama_models

# Restore specific file
borg extract F:\dockerDesktopFromBorgeBackup::2026-01-07_13-00-00 `
  app/main.py
```

### Browse Backup as Mounted Drive
```powershell
# Mount backup to Z: drive
borg mount F:\dockerDesktopFromBorgeBackup::2026-01-07_13-00-00 Z:\

# Browse files in Windows Explorer at Z:\
# Copy what you need

# Unmount when done
borg umount Z:\
```

---

## 5. Vorta GUI Setup

### Launch Vorta
```powershell
Start-Process "C:\Program Files\Vorta\Vorta.exe"
```

### Configure in Vorta:

1. **Add Repository**
   - Right-click Vorta system tray icon
   - "Repository" → "Add Existing Repository"
   - Path: `F:\dockerDesktopFromBorgeBackup`
   - Enter passphrase

2. **Add Source Folder**
   - "Sources" tab
   - Click "+ Add Folder"
   - Select: `D:\dev_env\Gravitas`

3. **Set Exclusions**
   - "Exclude" tab → "Add pattern"
   - Add each pattern:
     ```
     **/venv
     **/__pycache__
     **/*.pyc
     **/.git
     **/node_modules
     **/data/minio
     ```

4. **Configure Schedule**
   - "Schedule" tab
   - ✅ Enable "Backup automatically"
   - Interval: `Every 6 hours`
   - Prune: Keep `7 daily, 4 weekly, 6 monthly`

5. **Test Backup**
   - Click "Backup Now"
   - Watch progress in Vorta window

---

## 6. Backup Strategy (3-2-1 Rule)

### Current Setup:
- **Copy 1**: Working files on `D:\dev_env\Gravitas` (Primary - SSD)
- **Copy 2**: Borg backup on `F:\dockerDesktopFromBorgeBackup` (Secondary - Local)
- **Copy 3**: *(Recommended)* Weekly copy to external USB drive (Offsite)

### Recommended Schedule:
- **Automatic**: Every 6 hours (via Vorta)
- **Manual Full**: Weekly to external drive
- **Before Major Changes**: Manual backup before risky operations

---

## 7. Storage Estimates

| State | Size | Notes |
|-------|------|-------|
| Empty Gravitas | ~50MB | Code + configs only |
| With Models | ~20-30GB | Models + code + data |
| After 7 Days | ~25-35GB | With deduplication |
| After 30 Days | ~30-40GB | Incremental growth |

**Deduplication Example:**
- Day 1: Full 20GB backup
- Day 2: Only 100MB changes backed up (not another 20GB!)
- The 15GB model file is stored ONCE, shared across all archives

---

## 8. Emergency Recovery Procedures

### Scenario 1: Lost Single File
```powershell
# List backups
borg list F:\dockerDesktopFromBorgeBackup

# Extract just that file
borg extract F:\dockerDesktopFromBorgeBackup::2026-01-07_13-00-00 app/main.py
```

### Scenario 2: Lost Entire Database
```powershell
# Extract just database
borg extract F:\dockerDesktopFromBorgeBackup::2026-01-07_13-00-00 data/postgres_data
```

### Scenario 3: Total System Failure
```powershell
# 1. Reinstall BorgBackup on new system
# 2. Connect F: drive (or copy from external backup)
# 3. Full restore:
borg extract F:\dockerDesktopFromBorgeBackup::2026-01-07_13-00-00 `
  --target D:\dev_env\Gravitas

# 4. Verify files
cd D:\dev_env\Gravitas
ls
```

### Scenario 4: Model Files Corrupted
```powershell
# Remove corrupted models
Remove-Item -Recurse D:\dev_env\Gravitas\data\ollama_models\*

# Restore just models (saves re-downloading 15GB+!)
borg extract F:\dockerDesktopFromBorgeBackup::2026-01-07_13-00-00 data/ollama_models
```

---

## 9. Maintenance

### Check Backup Health
```powershell
# Verify repository consistency
borg check F:\dockerDesktopFromBorgeBackup

# Verify specific archive
borg check F:\dockerDesktopFromBorgeBackup::2026-01-07_13-00-00
```

### Prune Old Backups
```powershell
# Automatically remove old backups per retention policy
borg prune --keep-daily=7 --keep-weekly=4 --keep-monthly=6 `
  F:\dockerDesktopFromBorgeBackup
```

### Compact Repository (Free Space)
```powershell
# After pruning, compact to free disk space
borg compact F:\dockerDesktopFromBorgeBackup
```

---

## 10. Troubleshooting

### "Repository already exists" Error
```powershell
# If you need to re-initialize (WARNING: Deletes old backups!)
Remove-Item -Recurse -Force F:\dockerDesktopFromBorgeBackup\*
borg init --encryption=repokey F:\dockerDesktopFromBorgeBackup
```

### Forgot Passphrase
- **No recovery possible** - Borg uses strong encryption
- Start new repository with new passphrase
- Lesson: Store passphrase in password manager!

### Backup Too Slow
```powershell
# Use compression for faster backups (trade CPU for I/O)
borg create --compression lz4 F:\dockerDesktopFromBorgeBackup::"{now}" D:\dev_env\Gravitas
```

### Out of Disk Space on F:
```powershell
# Prune aggressively
borg prune --keep-daily=3 --keep-weekly=2 --keep-monthly=3 `
  F:\dockerDesktopFromBorgeBackup

# Compact to free space
borg compact F:\dockerDesktopFromBorgeBackup
```

---

## 11. Quick Reference

### Daily Commands
```powershell
# Manual backup
borg create F:\dockerDesktopFromBorgeBackup::"{now}" D:\dev_env\Gravitas

# List backups
borg list F:\dockerDesktopFromBorgeBackup

# Restore file
borg extract F:\dockerDesktopFromBorgeBackup::latest path/to/file
```

### System Tray (Vorta)
- Right-click icon → "Backup Now" (manual backup)
- Right-click icon → "Archives" (browse backups)
- Right-click icon → "Schedule" (check next backup time)

---

## 12. Backup Verification Checklist

Run this weekly to ensure backups are healthy:

```powershell
# 1. List recent backups
borg list F:\dockerDesktopFromBorgeBackup --last 7

# 2. Check repository health
borg check F:\dockerDesktopFromBorgeBackup

# 3. Verify critical files exist in latest backup
borg list F:\dockerDesktopFromBorgeBackup::latest | Select-String "docker-compose.yml"
borg list F:\dockerDesktopFromBorgeBackup::latest | Select-String "app/main.py"

# 4. Test restore of single file to temp location
New-Item -ItemType Directory -Path "C:\Temp\borg-test" -Force
cd C:\Temp\borg-test
borg extract F:\dockerDesktopFromBorgeBackup::latest README.md
cat README.md  # Verify it's correct
Remove-Item -Recurse C:\Temp\borg-test
```

✅ All checks pass = Backups are healthy!

---

## Support

- BorgBackup Docs: https://borgbackup.readthedocs.io/
- Vorta Docs: https://vorta.borgbase.com/
- Emergency Contact: Check `docs/GRAVITAS_SESSION_CONTEXT.md`

**Remember**: A backup you can't restore is not a backup at all. Test restores regularly!
