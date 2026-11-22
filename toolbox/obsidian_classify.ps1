$DESK = "C:\Users\ericz\Desktop"
$VAULT = "D:\B166ER-OpenClaw\workspace\obsidian-vault"
$ErrorActionPreference = 'SilentlyContinue'

# 帮助理解每个桌面文件夹里到底有什么
$dirs = @(
  '张实项目总控',
  '新媒体产品线',
  '小红书产品线',
  'AHL源代码',
  'AHL专利申请文件',
  '专利',
  '专利补正',
  '软著申请材料-AHL',
  '安逸集团_入职物料_20260707',
  '知局_完整版_v1.0',
  '自我革命',
  'AHL-BP-2026',
  '工作文档',
  '简历及应聘文件',
  '劳动合同',
  '小白的保单',
  '项目资料'
)

foreach ($d in $dirs) {
  $p = Join-Path $DESK $d
  if (-not (Test-Path $p)) { continue }
  Write-Host "=== $d ===" -ForegroundColor Cyan
  # 只看一级子目录
  $subs = Get-ChildItem $p -Directory
  $files = Get-ChildItem $p -File
  if ($subs) {
    Write-Host "  一级子目录:"
    $subs | Select-Object -First 25 | ForEach-Object {
      $cnt = (Get-ChildItem $_.FullName -Recurse -File -ErrorAction SilentlyContinue).Count
      "    [{0,4}] {1}" -f $cnt, $_.Name
    }
  }
  if ($files) {
    Write-Host "  直接文件:"
    $files | Select-Object -First 30 | ForEach-Object {
      $sz = "{0:N0}KB" -f ($_.Length/1KB)
      "    [{0,-8}] {1}" -f $sz, $_.Name
    }
  }
  Write-Host ""
}