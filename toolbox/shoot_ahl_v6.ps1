$html = 'D:\B166ER-OpenClaw\workspace\toolbox\ahl_infographic_v6.html'
$png = 'D:\B166ER-OpenClaw\workspace\toolbox\ahl_infographic_v6.png'
$url = 'file:///' + (($html -replace '\\','/'))
& 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe' --headless --disable-gpu --hide-scrollbars --no-sandbox --force-device-scale-factor=2 --window-size=1080,1920 --screenshot=$png $url 2>&1 | Out-Null
if (Test-Path $png) {
  $size = (Get-Item $png).Length
  Write-Output "OK: $png ($size bytes)"
} else {
  Write-Output 'FAIL: PNG not created'
}