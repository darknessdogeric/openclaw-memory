$path='D:\B166ER-OpenClaw\workspace\HEARTBEAT.md'
Write-Host '--- size ---'
(Get-Item $path).Length
Write-Host '--- last 30 lines ---'
Get-Content $path -Tail 30 -Encoding UTF8
