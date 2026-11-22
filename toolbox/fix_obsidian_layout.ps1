# 修复: 合并 mojibake 目录 + 清理 KB 误放
$vault = "D:\B166ER-OpenClaw\workspace\obsidian-vault"

Write-Host "=== 检查两个 01-日记 目录 ===" -ForegroundColor Cyan
$dirs01 = Get-ChildItem $vault -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name -like '01-*' }
foreach ($d in $dirs01) {
    Write-Host "  Found: [$($d.Name)] = $($d.FullName)"
    Get-ChildItem $d.FullName -File -Filter "*.md" -ErrorAction SilentlyContinue | Select-Object -First 3 | ForEach-Object { Write-Host "    - $($_.Name)" }
}

Write-Host "`n=== Step 1: 合并 mojibake 目录到正确目录 ===" -ForegroundColor Cyan
$sourceDir = Join-Path $vault (Get-ChildItem $vault -Directory | Where-Object { $_.Name -like '01-閺冦儴*' -or $_.Name -like '01-鏃ヨ*' } | Select-Object -ExpandProperty Name -First 1)
$correctName = "01-" + [char](0x65E5) + [char](0x8BB0)  # 01-日记
$targetDir = Join-Path $vault $correctName
Write-Host "  Source: $sourceDir"
Write-Host "  Target: $targetDir"

if (Test-Path $sourceDir) {
    if (-not (Test-Path $targetDir)) { New-Item -ItemType Directory -Path $targetDir -Force | Out-Null }
    Get-ChildItem $sourceDir -File -ErrorAction SilentlyContinue | ForEach-Object {
        $dst = Join-Path $targetDir $_.Name
        if (-not (Test-Path $dst)) {
            Copy-Item $_.FullName $dst -Force
            Write-Host "  COPY $($_.Name)" -ForegroundColor Green
        } else {
            Write-Host "  SKIP (exists): $($_.Name)" -ForegroundColor DarkGray
        }
    }
    Remove-Item $sourceDir -Recurse -Force
    Write-Host "  DEL mojibake dir" -ForegroundColor Yellow
} else {
    Write-Host "  mojibake dir not found (skip)" -ForegroundColor DarkGray
}

Write-Host "`n=== Step 2: 从 01-日记 移走 KB 文件 ===" -ForegroundColor Cyan
$kbName = "10-" + [char](0x6211) + [char](0x4E3A) + [char](0x4F60) + [char](0x751F) + [char](0x6210) + [char](0x7684)
$kbDir = Join-Path $vault $kbName
$kbTarget = Join-Path $kbDir ([char](0x77E5) + [char](0x8BC6) + [char](0x5E93))
$personaTarget = Join-Path $kbDir ([char](0x4EBA) + [char](0x683C) + [char](0x4E0E) + [char](0x8BA4) + [char](0x77E5))

if (Test-Path $targetDir) {
    $kbInDiary = Get-ChildItem $targetDir -File -Filter "*.md" -ErrorAction SilentlyContinue | Where-Object { $_.Name -notmatch '^\d{4}-\d{2}-\d{2}' }
    foreach ($f in $kbInDiary) {
        if ($f.Name -match ([char](0x77E5) + [char](0x8BC6) + [char](0x5E93))) {
            New-Item -ItemType Directory -Path $kbTarget -Force | Out-Null
            $dst = Join-Path $kbTarget $f.Name
            Copy-Item $f.FullName $dst -Force
            Write-Host "  KB -> $($dst)" -ForegroundColor Green
            Remove-Item $f.FullName -Force
        } elseif ($f.Name -match '人格|自我革命') {
            New-Item -ItemType Directory -Path $personaTarget -Force | Out-Null
            $dst = Join-Path $personaTarget $f.Name
            Copy-Item $f.FullName $dst -Force
            Write-Host "  PERSONA -> $($dst)" -ForegroundColor Green
            Remove-Item $f.FullName -Force
        } else {
            Write-Host "  KEEP: $($f.Name)" -ForegroundColor DarkGray
        }
    }
}

Write-Host "`n=== Step 3: 最终验证 ===" -ForegroundColor Cyan
Write-Host "01-日记 目录:"
if (Test-Path $targetDir) {
    Get-ChildItem $targetDir -File -Filter "*.md" -ErrorAction SilentlyContinue | Select-Object Name, Length | Format-Table -AutoSize
}

Write-Host "`n10-我为你生成的/知识库/:"
if (Test-Path $kbTarget) {
    Get-ChildItem $kbTarget -File -Filter "*.md" -ErrorAction SilentlyContinue | Select-Object Name, Length | Format-Table -AutoSize
}

Write-Host "`n10-我为你生成的/人格与认知/:"
if (Test-Path $personaTarget) {
    Get-ChildItem $personaTarget -File -Filter "*.md" -ErrorAction SilentlyContinue | Select-Object Name, Length | Format-Table -AutoSize
}
