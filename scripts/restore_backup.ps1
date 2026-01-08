# Restore a Gravitas backup
# Usage: .\scripts\restore_backup.ps1 <archive-name> [target-path]

param(
    [Parameter(Mandatory=$true)]
    [string]$ArchiveName,
    
    [Parameter(Mandatory=$false)]
    [string]$TargetPath = "D:\dev_env\Gravitas-RESTORED"
)

$REPO_PATH = "F:\dockerDesktopFromBorgeBackup"

Write-Host "=== Restoring Gravitas Backup ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Archive: $ArchiveName" -ForegroundColor Yellow
Write-Host "Target: $TargetPath" -ForegroundColor Yellow
Write-Host ""

# Confirm
$confirm = Read-Host "This will extract backup to $TargetPath. Continue? (y/n)"
if ($confirm -ne 'y') {
    Write-Host "Restore cancelled" -ForegroundColor Yellow
    exit 0
}

# Create target directory
New-Item -ItemType Directory -Path $TargetPath -Force | Out-Null

# Extract
& borg extract --progress "${REPO_PATH}::${ArchiveName}" --target $TargetPath

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✓ Restore completed successfully!" -ForegroundColor Green
    Write-Host "Files restored to: $TargetPath" -ForegroundColor Cyan
} else {
    Write-Host "✗ Restore failed!" -ForegroundColor Red
    exit 1
}
