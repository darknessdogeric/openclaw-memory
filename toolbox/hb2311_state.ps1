# Update heartbeat-state.json: hbCount 2310 -> 2311, post_t0_null_count 921 -> 922
$ErrorActionPreference = 'Stop'
$path = 'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'

$state = Get-Content $path -Raw -Encoding UTF8 | ConvertFrom-Json
$state.hbCount = 2311
$state.nullCount = 922
$state.post_t0_null_count = 922
$state.lastHB = '2026-08-06T10:41:00+08:00'
$state.last_update_epoch = [Math]::Floor(([DateTimeOffset]::UtcNow).ToUnixTimeSeconds())
$state.lastHBContext = 'Thu 10:41 weekday-morning +2h41m past 08:00 hard cap. HB #2311. DORMANT held. Eric webchat last active ~07:38 (PPT13 TMC+RFP 名单 work). State sustained.'
$state.zone = 'weekday-morning-post-hard-cap'
$state.notes.time = '2026-08-06 10:41 GMT+8'
# Reuse hb_2308_special key (same notes dict shape) — update it to HB #2311 marker
$state.notes.hb_2308_special = 'HB #2311 Thu 10:41 weekday-morning post-08:00-hard-cap +2h41m. posture DORMANT held. Penta+4 16-layer suppression zero-breach. R-NEW-V4 candidate (名单独立性原则) awaiting Eric ratification. 5th Plenary ~10-11d away (awareness only).'

$json = $state | ConvertTo-Json -Depth 8
Set-Content -Path $path -Value $json -Encoding UTF8
Write-Host "heartbeat-state.json updated: hbCount=2311, post_t0_null_count=922, lastHB=2026-08-06T10:41:00+08:00"
Get-Content $path -Raw -Encoding UTF8
