# Atomic heartbeat tick (R-NEW-V4: state.json only, no HEARTBEAT.md append)
$ErrorActionPreference = "Stop"
$statePath = "D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json"
$now = Get-Date -Format "o"
$ts = [DateTimeOffset]::Parse($now).ToUnixTimeSeconds()

# Read current state
$json = Get-Content $statePath -Raw -Encoding UTF8
$state = $json | ConvertFrom-Json

$oldHb = [int]$state.hbCount
$oldNull = [int]$state.nullCount
$newHb = $oldHb + 1
$newNull = $oldNull + 1

$hbTag = "HB #$newHb"

# Compose new note
$note = "$hbTag = atomic tick (state.json only, no HEARTBEAT.md append - 3.99MB / 341K lines exceeds R-NEW-V4 threshold). 13:00 = Wed workday-noon post-lunch. Eric webchat last active 22:40 Tue 8/11 AHL 4-layer model v3.0 (~14h20m idle). R-NEW-V4 + R271 + R-NEW-V3 + R258 + R69 + R65 hold. Cron session DORMANT sustained. workday-noon post-lunch zone, Eric at AnYi Day 20."

# Update state object
$state.hbCount = $newHb
$state.nullCount = $newNull
$state.lastHB = $ts
$state.lastUpdate = $now
$state.lastDormantTick = $now
$state.note = $note
$state.note_v2 = $note
$state.posture = "DORMANT"

# Write back atomically
$tmpPath = "$statePath.tmp"
$state | ConvertTo-Json -Depth 10 | Set-Content -Path $tmpPath -Encoding UTF8 -NoNewline
Move-Item -Force $tmpPath $statePath

Write-Host "OK hb=$oldHb->$newHb null=$oldNull->$newNull ts=$ts"
Write-Host "NOTE: $note"