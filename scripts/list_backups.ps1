# List all Gravitas backups

$REPO_PATH = "F:\dockerDesktopFromBorgeBackup"

Write-Host "=== Gravitas Backups ===" -ForegroundColor Cyan
Write-Host ""

& borg list $REPO_PATH

Write-Host ""
Write-Host "To restore a backup: .\scripts\restore_backup.ps1 <archive-name>" -ForegroundColor Yellow
Write-Host "To see details: borg info $REPO_PATH::<archive-name>" -ForegroundColor Yellow
