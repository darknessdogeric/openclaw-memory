$VAULT = "C:\Users\ericz\Documents\Obsidian Vault"
$ErrorActionPreference = 'SilentlyContinue'

Write-Host "=== Vault 顶层 ==="
Get-ChildItem $VAULT -Depth 0 | Select-Object Mode, Name, @{n='Size';e={"{0:N1}MB" -f ($_.Length/1MB)}} | Format-Table

Write-Host "`n=== Vault 顶层 .md (入口 / README / MOC) ==="
Get-ChildItem $VAULT -File -Filter "*.md" -Depth 0 | Select-Object Name, @{n='KB';e={[int]($_.Length/1024)}} | Format-Table

Write-Host "`n=== Vault 一级子目录 ==="
Get-ChildItem $VAULT -Directory | Select-Object Name | Format-Table -HideTableHeaders