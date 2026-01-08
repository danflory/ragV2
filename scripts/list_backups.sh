#!/bin/bash
# List all Gravitas backups

REPO_PATH="/mnt/f/dockerDesktopFromBorgeBackup"

echo "=== Gravitas Backups ==="
echo ""

borg list "$REPO_PATH"

echo ""
echo "To restore a backup: ./scripts/restore_backup.sh <archive-name>"
echo "To see details: borg info $REPO_PATH::<archive-name>"
