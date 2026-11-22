$DESK = "C:\Users\ericz\Desktop"
$VAULT = "D:\B166ER-OpenClaw\workspace\obsidian-vault"
$ErrorActionPreference = 'SilentlyContinue'

Write-Host "=== 桌面 .md 按一级目录分布 ==="
Get-ChildItem $DESK -Directory | ForEach-Object {
  $md = @(Get-ChildItem $_.FullName -Recurse -File -Filter "*.md")
  if ($md.Count -gt 0) {
    "{0,-30} md={1,4}" -f $_.Name, $md.Count
  }
}

Write-Host "`n=== 桌面 .md 总数 vs vault ==="
$deskMd = @(Get-ChildItem $DESK -Recurse -File -Filter "*.md")
$vaultMd = @(Get-ChildItem $VAULT -Recurse -File -Filter "*.md")
Write-Host "桌面 .md 总数: $($deskMd.Count)"
Write-Host "Vault .md 总数: $($vaultMd.Count)"

Write-Host "`n=== 桌面 .md 文件名样本 (前 60 个) ==="
$deskMd | Select-Object -First 60 FullName | ForEach-Object {
  $_.FullName.Replace($DESK, "[Desktop]")
}

Write-Host "`n=== 看桌面 .md 与 vault .md 是否有同名/重叠 (粗匹配文件名) ==="
$vaultNames = $vaultMd | ForEach-Object { $_.Name.ToLower() }
$deskNames = $deskMd | ForEach-Object { $_.Name.ToLower() }
$common = $deskNames | Where-Object { $_ -in $vaultNames }
Write-Host "同名文件数 (按文件名): $($common.Count)"

Write-Host "`n=== 桌面非 .md 文件类型分布 ==="
Get-ChildItem $DESK -Recurse -File | Where-Object { $_.Extension -ne '.md' } | Group-Object Extension | Sort-Object Count -Descending | Select-Object -First 20 Count, Name | Format-Table