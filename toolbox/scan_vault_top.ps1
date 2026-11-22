$ErrorActionPreference = 'SilentlyContinue'

# 1. D:\obsidian 顶层 (不递归)
Write-Host "=== D:\obsidian 顶层 ==="
Get-ChildItem "D:\obsidian" -Directory | Select-Object -ExpandProperty Name
Write-Host ""
Write-Host "--- 顶层 .md ---"
Get-ChildItem "D:\obsidian" -File -Filter "*.md" -Depth 0 | Select-Object Name, @{n='KB';e={[int]($_.Length/1024)}}
Write-Host ""
Write-Host "--- 顶层其它文件 ---"
Get-ChildItem "D:\obsidian" -File -Depth 0 | Where-Object { $_.Extension -ne ".md" } | Select-Object Name | Format-Table -HideTableHeaders