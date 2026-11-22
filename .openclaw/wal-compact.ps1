$ErrorActionPreference = 'Continue'
$repo = Join-Path $env:USERPROFILE 'Backups\openclaw-sqlite'

function Get-WalSummary {
    $files = Get-ChildItem -Path $env:USERPROFILE -Recurse -Filter '*.db-wal' -ErrorAction SilentlyContinue
    if ($files) {
        $total = ($files | Measure-Object -Property Length -Sum).Sum
        return "count=$($files.Count) total=$total bytes"
    }
    return "no WAL files found under $env:USERPROFILE"
}

Write-Host '=== WAL BEFORE ==='
Write-Host (Get-WalSummary)

Write-Host '=== BACKUP OUTPUT ==='
try {
    $output = openclaw backup sqlite create --global --repository $repo --json 2>&1
    $exitCode = $LASTEXITCODE
    Write-Host "exit=$exitCode"
    Write-Host '---'
    $output | ForEach-Object { Write-Host $_ }
} catch {
    Write-Host "exception: $_"
}

Write-Host '=== WAL AFTER ==='
Write-Host (Get-WalSummary)

Write-Host '=== REPO LIST ==='
if (Test-Path $repo) {
    Get-ChildItem -Path $repo -Recurse -ErrorAction SilentlyContinue | Select-Object FullName,Length,LastWriteTime | Format-Table -AutoSize
} else {
    Write-Host "repo path does not exist: $repo"
}
