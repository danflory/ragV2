# Gravitas Manual Backup Script
# Run this anytime to create a backup

Write-Host "=== Creating Gravitas Backup ===" -ForegroundColor Cyan
Write-Host ""

# Configuration
$REPO_PATH = "F:\dockerDesktopFromBorgeBackup"
$SOURCE_PATH = "D:\dev_env\Gravitas"
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"

# Check if repository exists
if (!(Test-Path "$REPO_PATH\config")) {
    Write-Host "✗ Repository not initialized!" -ForegroundColor Red
    Write-Host "Run setup first: .\scripts\setup_backup.ps1" -ForegroundColor Yellow
    exit 1
}

# Create backup
Write-Host "Backing up: $SOURCE_PATH" -ForegroundColor Yellow
Write-Host "To: $REPO_PATH::$timestamp" -ForegroundColor Yellow
Write-Host ""

& borg create --stats --progress `
    --exclude '**/venv' `
    --exclude '**/__pycache__' `
    --exclude '**/*.pyc' `
    --exclude '.git' `
    --exclude '**/node_modules' `
    --exclude '**/data/minio' `
    "${REPO_PATH}::${timestamp}" `
    $SOURCE_PATH

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✓ Backup completed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Archive name: $timestamp" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "View all backups: borg list $REPO_PATH" -ForegroundColor White
} else {
    Write-Host "✗ Backup failed!" -ForegroundColor Red
    exit 1
}
