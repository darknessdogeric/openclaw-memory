$VAULT = "D:\B166ER-OpenClaw\workspace\obsidian-vault"
$ErrorActionPreference = 'SilentlyContinue'

Write-Host "=== Vault 一级子目录文件统计 ==="
Get-ChildItem $VAULT -Directory | ForEach-Object {
  $all = Get-ChildItem $_.FullName -Recurse -File
  $count = $all.Count
  $size = "{0:N2}MB" -f (($all | Measure-Object Length -Sum).Sum / 1MB)
  $md = ($all | Where-Object { $_.Extension -eq '.md' }).Count
  $other = $count - $md
  $depth2 = (Get-ChildItem $_.FullName -Directory).Count
  "{0,-30} files={1,4} md={2,4} subdirs={3,3} size={4}" -f $_.Name, $count, $md, $depth2, $size
}

Write-Host "`n=== Vault 总览 ==="
$all = Get-ChildItem $VAULT -Recurse -File
$md = $all | Where-Object { $_.Extension -eq '.md' }
Write-Host "总文件: $($all.Count)"
Write-Host "总 .md: $($md.Count)"
$totalMB = "{0:N2}MB" -f (($all | Measure-Object Length -Sum).Sum / 1MB)
Write-Host "总大小: $totalMB"
Write-Host ""
Write-Host "=== 文件类型分布 ==="
$all | Group-Object Extension | Sort-Object Count -Descending | Select-Object -First 15 Count, Name | Format-Table

Write-Host "`n=== 顶层 .md / 关键入口 ==="
Get-ChildItem $VAULT -Recurse -File -Filter "*.md" | Where-Object {
  $_.DirectoryName -eq $VAULT -or $_.Name -like 'MOC*' -or $_.Name -like 'README*' -or $_.Name -like '*索引*' -or $_.Name -like '*Index*' -or $_.Name -like '*Map*' -or $_.Name -like '*欢迎*'
} | Select-Object FullName | Format-Table -HideTableHeaders -Wrap