# Obsidian 全盘扫描 - 摸清家底
$ErrorActionPreference = 'SilentlyContinue'

Write-Host "=== 1. 桌面顶层目录 (C:\Users\ericz\Desktop) ==="
Get-ChildItem "C:\Users\ericz\Desktop" -Directory | Select-Object Name | Format-Table -HideTableHeaders

Write-Host "`n=== 2. D 盘根目录 ==="
Get-ChildItem D:\ -Directory | Select-Object Name | Format-Table -HideTableHeaders

Write-Host "`n=== 3. 几个候选路径存在性 ==="
$paths = @(
  'D:\桌面张实项目总控',
  'D:\AHL-Database',
  'D:\张实项目总控',
  'D:\AHL',
  'D:\项目',
  'D:\我的文档',
  'D:\Documents',
  'C:\Users\ericz\Documents',
  'C:\Users\ericz\AHL-Database',
  'C:\Users\ericz\Desktop\AHL-BP-2026',
  'C:\Users\ericz\Desktop\张实项目总控',
  'C:\Users\ericz\Desktop\项目资料'
)
foreach ($p in $paths) {
  if (Test-Path $p) { Write-Host "[HIT] $p" } else { Write-Host "[-- ] $p" }
}

Write-Host "`n=== 4. 桌面子目录文件数 ==="
Get-ChildItem "C:\Users\ericz\Desktop" -Directory | ForEach-Object {
  $count = (Get-ChildItem $_.FullName -Recurse -File | Measure-Object).Count
  $size = "{0:N1}MB" -f ((Get-ChildItem $_.FullName -Recurse -File | Measure-Object Length -Sum).Sum / 1MB)
  "{0,-30} files={1,5}  size={2}" -f $_.Name, $count, $size
}

Write-Host "`n=== 5. 桌面文件类型统计 ==="
Get-ChildItem "C:\Users\ericz\Desktop" -Recurse -File | Group-Object Extension | Sort-Object Count -Descending | Select-Object -First 25 Count, Name | Format-Table