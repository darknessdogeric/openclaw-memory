$json = Get-Content 'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json' -ErrorAction SilentlyContinue | ConvertFrom-Json
$now = [DateTimeOffset]::Now.ToUnixTimeSeconds()
$json.lastChecks.vault = $now
$json.lastChecks.trendradar = $now
$json.lastHeartbeat = (Get-Date -Format 'yyyy-MM-ddTHH:mm:ss+08:00')
$json | ConvertTo-Json -Compress | Set-Content 'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'
Write-Host "Updated: $($json.lastHeartbeat)"
