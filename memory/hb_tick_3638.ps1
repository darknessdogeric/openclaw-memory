$path = 'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'
if (Test-Path $path) {
    $s = Get-Content $path -Raw | ConvertFrom-Json
    $s.hbCount = 3638
    $s.lastTick = '2026-08-21T12:15:00+08:00'
    $tmp = $path + '.tmp'
    $s | ConvertTo-Json -Depth 4 | Out-File -FilePath $tmp -Encoding utf8
    Move-Item -Force $tmp $path
    Write-Output 'hbCount=3638 atomic-tick OK'
} else {
    Write-Output 'no state.json'
}