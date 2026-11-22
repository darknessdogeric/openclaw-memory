function Sync-MdFile {
    param([string]$src, [string]$dst)
    $dstDir = Split-Path $dst -Parent
    New-Item -ItemType Directory -Path $dstDir -Force | Out-Null
    Copy-Item $src $dst -Force
    $info = Get-Item $dst
    Write-Host "  OK  $((Get-Item $src).Name) -> $($_.Name) ($($info.Length)b)" -ForegroundColor Green
}

Write-Host "=== Step 1: 清理 01-日记/ 误放的非日记文件 ===" -ForegroundColor Cyan
$misplaced = Get-ChildItem "D:\B166ER-OpenClaw\workspace\obsidian-vault\01-日记" -File -Filter "*.md" -ErrorAction SilentlyContinue | Where-Object { $_.Name -notmatch '^\d{4}-\d{2}-\d{2}\.md$' }
foreach ($f in $misplaced) {
    Write-Host "  DEL $($f.Name)" -ForegroundColor Yellow
    Remove-Item $f.FullName -Force
}

Write-Host "`n=== Step 2: 同步 7 月日记 (精确) ===" -ForegroundColor Cyan
$diaryFiles = Get-ChildItem "D:\B166ER-OpenClaw\workspace\memory" -File -Filter "2026-07-*.md" -ErrorAction SilentlyContinue | Sort-Object Name -Descending
foreach ($f in $diaryFiles) {
    Sync-MdFile -src $f.FullName -dst "D:\B166ER-OpenClaw\workspace\obsidian-vault\01-日记\$($f.Name)"
}

Write-Host "`n=== Step 3: KB 文件 -> 10-我为你生成的/知识库/ ===" -ForegroundColor Cyan
$kbFiles = Get-ChildItem "D:\B166ER-OpenClaw\workspace\memory" -File -Filter "*知识库*.md" -ErrorAction SilentlyContinue
foreach ($f in $kbFiles) {
    Sync-MdFile -src $f.FullName -dst "D:\B166ER-OpenClaw\workspace\obsidian-vault\10-我为你生成的\知识库\$($f.Name)"
}

Write-Host "`n=== Step 4: 人格/认知系列 -> 10-我为你生成的/人格与认知/ ===" -ForegroundColor Cyan
$personaFiles = Get-ChildItem "D:\B166ER-OpenClaw\workspace\memory" -File -Filter "*.md" -ErrorAction SilentlyContinue | Where-Object { $_.Name -match '人格|自我革命' }
foreach ($f in $personaFiles) {
    Sync-MdFile -src $f.FullName -dst "D:\B166ER-OpenClaw\workspace\obsidian-vault\10-我为你生成的\人格与认知\$($f.Name)"
}

Write-Host "`n=== Step 5: 验证 01-日记/ ===" -ForegroundColor Cyan
Get-ChildItem "D:\B166ER-OpenClaw\workspace\obsidian-vault\01-日记" -File -Filter "*.md" -ErrorAction SilentlyContinue | Select-Object Name, Length | Format-Table -AutoSize

Write-Host "`n=== Step 6: 验证整体结构 ===" -ForegroundColor Cyan
Get-ChildItem "D:\B166ER-OpenClaw\workspace\obsidian-vault" -Recurse -File -Filter "*.md" -ErrorAction SilentlyContinue | Group-Object DirectoryName | ForEach-Object {
    Write-Host "`n[$($_.Name)]"
    $_.Group | Select-Object -First 8 | ForEach-Object { Write-Host "  $($_.Name) ($($_.Length)b)" }
}
