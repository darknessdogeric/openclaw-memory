$f = 'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'
$j = Get-Content $f -Raw | ConvertFrom-Json
$j.lastHeartbeat = (Get-Date).ToString('yyyy-MM-ddTHH:mm:sszzz')
$j.hbCount = [int]$j.hbCount + 1
$j | ConvertTo-Json -Depth 10 | Set-Content $f -Encoding UTF8
Write-Host ("HB #" + $j.hbCount + " recorded")
