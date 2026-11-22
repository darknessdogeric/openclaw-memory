# B166ER 每周全量备份脚本
# Cron: 周日 03:00 触发
# Source: D:\B166ER-OpenClaw\workspace + D:\B166ER-OpenClaw\workspace\obsidian-vault
# Target: D:\B166ER-Backup\weekly\2026-07-19\

param(
    [string]$Date = (Get-Date -Format 'yyyy-MM-dd')
)

$ErrorActionPreference = 'Continue'
$today = $Date
$backupRoot = 'D:\B166ER-Backup\weekly\' + $today
$wsSrc = 'D:\B166ER-OpenClaw\workspace'
$vSrc = 'D:\B166ER-OpenClaw\workspace\obsidian-vault'

Write-Host "=== B166ER Weekly Backup $today ==="
Write-Host "Target: $backupRoot"

# 0. 准备目标目录
if (-not (Test-Path $backupRoot)) { New-Item -ItemType Directory -Path $backupRoot | Out-Null }
$wsDst = Join-Path $backupRoot 'workspace'
$vDst = Join-Path $backupRoot 'vault'

# 1. 先统计源目录文件数和大小（用于汇报）
Write-Host "`n--- 源目录扫描 ---"
$wsItems = Get-ChildItem $wsSrc -Recurse -Force -ErrorAction SilentlyContinue | Where-Object { -not $_.PSIsContainer }
$wsCount = $wsItems.Count
$wsSize = ($wsItems | Measure-Object Length -Sum).Sum
Write-Host "workspace: $wsCount files, $([math]::Round($wsSize/1GB,2)) GB"

$vItems = Get-ChildItem $vSrc -Recurse -Force -ErrorAction SilentlyContinue | Where-Object { -not $_.PSIsContainer }
$vCount = $vItems.Count
$vSize = ($vItems | Measure-Object Length -Sum).Sum
Write-Host "vault: $vCount files, $([math]::Round($vSize/1MB,1)) MB"

# 2. robocopy workspace（排除 node_modules / 缓存 / 临时目录）
Write-Host "`n--- workspace robocopy ---"
$wsStart = Get-Date
$wsLog = Join-Path $backupRoot 'workspace-backup.log'
# /MIR 镜像（删目标里多余的），/R:3 重试3次 /W:5 间隔5s /MT:8 并行
$wsArgs = @(
    $wsSrc,
    $wsDst,
    '/MIR',
    '/R:3', '/W:5',
    '/MT:8',
    '/NP',
    '/BYTES',
    '/LOG+:"' + $wsLog + '"',
    # 排除大目录
    '/XD', 'node_modules', '.git', '.next', 'dist', '__pycache__', '.cache', '.playwright-cli', '.edge-screenshot', 'cache',
    # 排除临时文件
    '/XF', '*.tmp', '*.log.bak', '*.pyc'
)
$wsResult = & robocopy @wsArgs
$wsExit = $LASTEXITCODE
$wsElapsed = (Get-Date) - $wsStart
Write-Host "workspace exit=$wsExit, elapsed=$(($wsElapsed).ToString('mm\:ss'))"

# 3. robocopy vault（全量）
Write-Host "`n--- vault robocopy ---"
$vStart = Get-Date
$vLog = Join-Path $backupRoot 'vault-backup.log'
$vArgs = @(
    $vSrc,
    $vDst,
    '/MIR',
    '/R:3', '/W:5',
    '/MT:8',
    '/NP',
    '/BYTES',
    '/LOG+:"' + $vLog + '"'
)
$vResult = & robocopy @vArgs
$vExit = $LASTEXITCODE
$vElapsed = (Get-Date) - $vStart
Write-Host "vault exit=$vExit, elapsed=$(($vElapsed).ToString('mm\:ss'))"

# 4. 统计目标目录
Write-Host "`n--- 备份结果统计 ---"
$dWsItems = Get-ChildItem $wsDst -Recurse -Force -ErrorAction SilentlyContinue | Where-Object { -not $_.PSIsContainer }
$dWsCount = $dWsItems.Count
$dWsSize = ($dWsItems | Measure-Object Length -Sum).Sum
Write-Host "workspace backup: $dWsCount files, $([math]::Round($dWsSize/1GB,2)) GB"

$dVItems = Get-ChildItem $vDst -Recurse -Force -ErrorAction SilentlyContinue | Where-Object { -not $_.PSIsContainer }
$dVCount = $dVItems.Count
$dVSize = ($dVItems | Measure-Object Length -Sum).Sum
Write-Host "vault backup: $dVCount files, $([math]::Round($dVSize/1MB,1)) MB"

# 5. 写 manifest
$manifest = @{
    date = $today
    source = @{
        workspace_path = $wsSrc
        workspace_files = $wsCount
        workspace_size_gb = [math]::Round($wsSize/1GB, 2)
        vault_path = $vSrc
        vault_files = $vCount
        vault_size_mb = [math]::Round($vSize/1MB, 1)
    }
    backup = @{
        workspace_files = $dWsCount
        workspace_size_gb = [math]::Round($dWsSize/1GB, 2)
        vault_files = $dVCount
        vault_size_mb = [math]::Round($dVSize/1MB, 1)
        workspace_exit = $wsExit
        vault_exit = $vExit
        workspace_elapsed_min = [math]::Round($wsElapsed.TotalMinutes, 1)
        vault_elapsed_min = [math]::Round($vElapsed.TotalMinutes, 1)
    }
    target = $backupRoot
    finished_at = (Get-Date).ToString('yyyy-MM-dd HH:mm:ss')
}
$manifestPath = Join-Path $backupRoot 'backup-manifest.json'
$manifest | ConvertTo-Json -Depth 3 | Out-File -FilePath $manifestPath -Encoding utf8

Write-Host "`n=== 备份完成 ==="
Write-Host "manifest: $manifestPath"
Write-Host "ROBOCOPY exit codes: workspace=$wsExit vault=$vExit  (exit<=7 is success)"
