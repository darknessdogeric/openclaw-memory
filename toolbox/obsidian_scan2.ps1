$ErrorActionPreference = 'SilentlyContinue'

Write-Host "=== Vault 本体 (D:\obsidian) 顶层 ==="
Get-ChildItem "D:\obsidian" -Directory | Select-Object Name | Format-Table -HideTableHeaders

Write-Host "`n=== Vault 顶层 .md 文件 (看看有没有 README / MOC 入口) ==="
Get-ChildItem "D:\obsidian" -File -Filter "*.md" | Select-Object Name, Length | Format-Table

Write-Host "`n=== D 盘其它与知识相关的目录 ==="
$candidates = @('D:\酒店相关SOP','D:\my-project','D:\minimax','D:\B166ER-openclaw','D:\self-improving','D:\Users','D:\OpenHuman')
foreach ($p in $candidates) {
  if (Test-Path $p) {
    $count = (Get-ChildItem $p -Recurse -File | Measure-Object).Count
    $size = "{0:N1}MB" -f ((Get-ChildItem $p -Recurse -File | Measure-Object Length -Sum).Sum / 1MB)
    "{0,-40} files={1,5}  size={2}" -f $p, $count, $size
  }
}

Write-Host "`n=== 桌面上 .md 文件前 30 个 (看看是不是散落) ==="
Get-ChildItem "C:\Users\ericz\Desktop" -Recurse -File -Filter "*.md" | Select-Object -First 30 FullName | ForEach-Object { $_.FullName }

Write-Host "`n=== 张实项目总控 顶层 ==="
Get-ChildItem "C:\Users\ericz\Desktop\张实项目总控" -Directory | Select-Object Name | Format-Table -HideTableHeaders

Write-Host "`n=== 新媒体产品线 顶层 ==="
Get-ChildItem "C:\Users\ericz\Desktop\新媒体产品线" -Directory | Select-Object Name | Format-Table -HideTableHeaders