$jsonPath = 'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'
$json = Get-Content $jsonPath -Raw | ConvertFrom-Json
$json.hbCount = 2169
$json.nullCount = 767
$json.post_t0_null_count = 767
$json.lastChecks.heartbeat = [Math]::Floor((Get-Date -Date '2026-08-01 16:53:00+08:00').ToUniversalTime().Subtract([DateTime]'1970-01-01 00:00:00Z').TotalSeconds)
$json.lastHB = 'HB #2169 at 2026-08-01T16:53:00+08:00'
$json.lastHBContext = 'Sat 16:53 weekend-afternoon. Posture DORMANT held. nullCount 766->767 (767th consecutive null). +14min after HB #2168 within tolerance. Staying quiet per R65/R68/R69. AnYi D+9 sustained. Eric webchat sovereign. Last contact 16:16 Q pre-review national style.'
$json | ConvertTo-Json -Depth 5 | Set-Content $jsonPath -Encoding UTF8
Write-Output "OK hbCount=$($json.hbCount) nullCount=$($json.nullCount)"