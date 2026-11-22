$ErrorActionPreference = 'SilentlyContinue'

Write-Host "=== 找 .obsidian 配置目录 (Vault 标记) ==="
# 在常见位置找 .obsidian 配置
$roots = @(
  'D:\',
  'C:\Users\ericz\Documents',
  'C:\Users\ericz\Desktop',
  'C:\Users\ericz\OneDrive',
  'D:\OneDrive'
)

# 用 Get-PSDrive 列出可用盘符
Get-PSDrive -PSProvider FileSystem | Where-Object { $_.Used -gt 0 } | ForEach-Object {
  $drive = $_.Root
  Write-Host "扫描盘符: $drive"
  Get-ChildItem -Path $drive -Filter ".obsidian" -Directory -ErrorAction SilentlyContinue -Force | Select-Object -First 5 FullName
}

Write-Host ""
Write-Host "=== 已知 Vault 根 (根据 vault_index 看 00-Workspace-核心 等结构) ==="
# vault_index 报告了 10-我为你生成的 等目录, 直接找
$candidate = "D:\Users\ericz\Desktop\张实项目总控"
if (Test-Path $candidate) { Write-Host "[HIT] $candidate" }
# 一些常见的 vault 位置
foreach ($p in @(
  'D:\Users\ericz',
  'D:\Users\ericz\Documents',
  'D:\Users\ericz\Documents\Obsidian',
  'D:\Users\ericz\Documents\ObsidianVault',
  'D:\Users\ericz\Desktop\Obsidian',
  'C:\Users\ericz\Documents\Obsidian',
  'C:\Users\ericz\Documents\Vault',
  'C:\Users\ericz\OneDrive\Documents\Obsidian',
  'D:\Users\ericz\Desktop\知局_完整版_v1.0'
)) {
  if (Test-Path $p) { Write-Host "[HIT] $p" }
}