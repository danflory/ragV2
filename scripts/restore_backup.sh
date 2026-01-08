#!/bin/bash
# Restore a Gravitas backup
# Usage: ./scripts/restore_backup.sh <archive-name> [target-path]

set -e

REPO_PATH="/mnt/f/dockerDesktopFromBorgeBackup"
ARCHIVE_NAME="$1"
TARGET_PATH="${2:-/home/dflory/dev_env/Gravitas-RESTORED}"

if [ -z "$ARCHIVE_NAME" ]; then
    echo "Usage: $0 <archive-name> [target-path]"
    echo ""
    echo "Available archives:"
    borg list "$REPO_PATH"
    exit 1
fi

echo "=== Restoring Gravitas Backup ==="
echo ""
echo "Archive: $ARCHIVE_NAME"
echo "Target: $TARGET_PATH"
echo ""

# Confirm
read -p "This will extract backup to $TARGET_PATH. Continue? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Restore cancelled"
    exit 0
fi

# Create target directory
mkdir -p "$TARGET_PATH"

# Extract
cd "$TARGET_PATH"
borg extract --progress "${REPO_PATH}::${ARCHIVE_NAME}"

echo ""
echo "✓ Restore completed successfully!"
echo "Files restored to: $TARGET_PATH"
