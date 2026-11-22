$f = 'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md'
Write-Host ('Size: ' + (Get-Item $f).Length + ' bytes')
Write-Host '--- Last 25 lines ---'
Get-Content $f -Tail 25 -Encoding UTF8
