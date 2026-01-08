# Gravitas Backup - Quick Start (WSL/Ubuntu)

## Run These Commands in Ubuntu/WSL Terminal

### First Time Setup (Run Once)

```bash
# Open Ubuntu/WSL terminal, then:

# Navigate to Gravitas
cd /home/dflory/dev_env/Gravitas

# Run setup script (installs Borg + creates first backup)
./scripts/setup_backup.sh
```

**IMPORTANT**: The setup will ask for a **passphrase**. Choose a strong one and WRITE IT DOWN!

---

## Daily Use

### Create Manual Backup
```bash
cd /home/dflory/dev_env/Gravitas
./scripts/backup_now.sh
```

### List All Backups
```bash
cd /home/dflory/dev_env/Gravitas
./scripts/list_backups.sh
```

### Restore a Backup
```bash
cd /home/dflory/dev_env/Gravitas
./scripts/restore_backup.sh 2026-01-07_13-30-00
```

Or restore to custom location:
```bash
./scripts/restore_backup.sh 2026-01-07_13-30-00 /home/dflory/dev_env/Gravitas-RESTORED
```

---

## How to Open Ubuntu/WSL Terminal

### From Windows:
1. **Press Win + R** → type `ubuntu` → Enter
2. **Or** Search for "Ubuntu" in Start Menu
3. **Or** In PowerShell: `wsl`

### Quick Access from Windows Terminal:
- Open Windows Terminal → Select "Ubuntu" tab

---

## Automatic Backups (Optional - Cron)

Set up automatic backups every 6 hours:

```bash
# Edit cron jobs
crontab -e

# Add this line (runs every 6 hours):
0 */6 * * * /home/dflory/dev_env/Gravitas/scripts/backup_now.sh >> /home/dflory/dev_env/Gravitas/backup.log 2>&1

# Save and exit (Ctrl+X, then Y, then Enter)
```

---

## What's Backed Up

✅ All code in `app/`, `tests/`, `docs/`  
✅ Model files in `data/ollama_models/` (15GB+)  
✅ Database in `data/postgres_data/`  
✅ Vector DB in `data/qdrant/`  
✅ Config files (`docker-compose.yml`, `.env`, etc.)  

❌ Virtual environments (`venv/`)  
❌ Cache files (`__pycache__/`, `*.pyc`)  
❌ Git history (`.git/`)  

---

## Storage Location

- **Backups stored**: `/mnt/f/dockerDesktopFromBorgeBackup/` (F: drive from WSL)
- **Source**: `/home/dflory/dev_env/Gravitas/`

---

## Quick Borg Commands (Direct Access)

```bash
# List backups
borg list /mnt/f/dockerDesktopFromBorgeBackup

# Show backup info
borg info /mnt/f/dockerDesktopFromBorgeBackup::2026-01-07_13-30-00

# Mount backup as folder (browse old files)
mkdir /tmp/backup-mount
borg mount /mnt/f/dockerDesktopFromBorgeBackup::2026-01-07_13-30-00 /tmp/backup-mount
cd /tmp/backup-mount
# Browse files, copy what you need
cd ~
borg umount /tmp/backup-mount

# Check repository health
borg check /mnt/f/dockerDesktopFromBorgeBackup

# Prune old backups
borg prune --keep-daily=7 --keep-weekly=4 --keep-monthly=6 /mnt/f/dockerDesktopFromBorgeBackup
```

---

## Troubleshooting

### "Permission denied" error
Make sure scripts are executable:
```bash
chmod +x /home/dflory/dev_env/Gravitas/scripts/*.sh
```

### Can't access F: drive
Check if F: is mounted in WSL:
```bash
ls /mnt/f/
# If empty or error, mount it:
sudo mkdir -p /mnt/f
sudo mount -t drvfs F: /mnt/f
```

### Installation issues
```bash
# Update package lists
sudo apt update

# Install BorgBackup
sudo apt install borgbackup -y

# Verify installation
borg --version
```

---

## Full Documentation

See `docs/BACKUP_SETUP.md` for complete documentation including:
- Emergency recovery procedures
- Advanced restore options
- Maintenance commands
- Storage estimates
