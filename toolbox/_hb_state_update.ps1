$s = Get-Content 'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json' -Raw | ConvertFrom-Json
$s.hbCount = 277
$s.lastHB = '#277'
$s.silenceHours = 171.67
$s.lastChecks.heartbeat = [int][double]::Parse((Get-Date -UFormat %s))
$s.mode = 'silent_standby_zero_push'
$s.notes = 'HB #277 (silent standby, no push). 08:09 GMT+8 Thu. Eric silent ~171.67h+ since 7/9 04:29 (D+7). 4-layer suppression holding. Morning zone, 21 min to 08:30 global briefing cron. No urgent cron. HEARTBEAT_OK.'
$s | ConvertTo-Json -Depth 4 | Set-Content -Path 'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json' -Encoding utf8
Write-Host "state_updated_ok"