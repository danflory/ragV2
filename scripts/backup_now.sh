#!/bin/bash
# Gravitas Manual Backup Script (WSL/Ubuntu)
# Run this anytime to create a backup

set -e

echo "=== Creating Gravitas Backup ==="
echo ""

# Configuration
REPO_PATH="/mnt/f/dockerDesktopFromBorgeBackup"
SOURCE_PATH="/home/dflory/dev_env/Gravitas"
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)

# Check if repository exists
if [ ! -f "$REPO_PATH/config" ]; then
    echo "✗ Repository not initialized!"
    echo "Run setup first: ./scripts/setup_backup.sh"
    exit 1
fi

# Create backup
echo "Backing up: $SOURCE_PATH"
echo "To: $REPO_PATH::$TIMESTAMP"
echo ""

cd "$SOURCE_PATH"
borg create --stats --progress \
    --exclude '**/venv' \
    --exclude '**/__pycache__' \
    --exclude '**/*.pyc' \
    --exclude '.git' \
    --exclude '**/node_modules' \
    --exclude '**/data/minio' \
    "${REPO_PATH}::${TIMESTAMP}" \
    .

echo ""
echo "✓ Backup completed successfully!"
echo ""
echo "Archive name: $TIMESTAMP"
echo ""
echo "View all backups: borg list $REPO_PATH"
