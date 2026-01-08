#!/bin/bash
# Gravitas Backup Setup Script (WSL/Ubuntu)
# Run this ONCE to initialize BorgBackup

set -e

echo "=== Gravitas Backup Setup (WSL/Ubuntu) ==="
echo ""

# Configuration
REPO_PATH="/mnt/f/dockerDesktopFromBorgeBackup"
SOURCE_PATH="/home/dflory/dev_env/Gravitas"

# Step 1: Check if BorgBackup is installed
echo "Checking for BorgBackup..."
if command -v borg &> /dev/null; then
    echo "✓ BorgBackup found: $(borg --version)"
else
    echo "✗ BorgBackup not found!"
    echo "Installing BorgBackup..."
    sudo apt update
    sudo apt install borgbackup -y
    echo "✓ BorgBackup installed: $(borg --version)"
fi

# Step 2: Create backup directory
echo ""
echo "Creating backup directory..."
mkdir -p "$REPO_PATH"
echo "✓ Directory created: $REPO_PATH"

# Step 3: Initialize Borg repository
echo ""
echo "Initializing Borg repository..."
echo "IMPORTANT: You will be asked for a passphrase."
echo "Choose a strong passphrase and WRITE IT DOWN!"
echo ""

if [ -f "$REPO_PATH/config" ]; then
    echo "✓ Repository already initialized at $REPO_PATH"
else
    borg init --encryption=repokey "$REPO_PATH"
    echo "✓ Repository initialized successfully!"
fi

# Step 4: Create first backup
echo ""
echo "Creating initial backup..."
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)

cd "$SOURCE_PATH"
borg create --stats --progress \
    --exclude '**/venv' \
    --exclude '**/__pycache__' \
    --exclude '**/*.pyc' \
    --exclude '.git' \
    --exclude '**/node_modules' \
    "${REPO_PATH}::${TIMESTAMP}" \
    .

echo ""
echo "✓ Initial backup created successfully!"

# Step 5: Summary
echo ""
echo "=== Setup Complete ==="
echo ""
echo "Repository: $REPO_PATH"
echo "Source: $SOURCE_PATH"
echo ""
echo "Next steps:"
echo "1. Run backup anytime: ./scripts/backup_now.sh"
echo "2. List backups: borg list $REPO_PATH"
echo "3. Schedule automatic backups with cron (optional)"
echo ""
echo "See docs/BACKUP_SETUP.md for full documentation"
