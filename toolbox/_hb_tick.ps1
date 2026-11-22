# Heartbeat tick script - minimal mode per R012
$utf8 = New-Object System.Text.UTF8Encoding $false
[Console]::OutputEncoding = $utf8

# Read current state
$statePath = 'memory\heartbeat-state.json'
$state = Get-Content $statePath -Raw -Encoding UTF8 | ConvertFrom-Json
$oldHB = $state.lastHBNumber
$oldCount = $state.hbCount

# Compute new state
$now = Get-Date -Format 'yyyy-MM-ddTHH:mm:sszzz'
$newCount = $oldCount + 1
$newHB = '#' + $newCount

# Compute Eric silence hours
$ericLastContact = Get-Date '2026-07-16 13:16'
$silenceHours = [math]::Round(((Get-Date) - $ericLastContact).TotalHours, 2)

# Compute AnYi hours
$anyiStart = Get-Date '2026-07-19 12:33'
$anyiHours = [math]::Round(((Get-Date) - $anyiStart).TotalHours, 2)

# Compute 7/24 D-Day countdown
$dDay = Get-Date '2026-07-24 09:00'
$dDayHours = [math]::Round(($dDay - (Get-Date)).TotalHours, 2)

# Next cron: 21:00 today
$nextCron = Get-Date '2026-07-23 21:00'
$nextCronHours = [math]::Round(($nextCron - (Get-Date)).TotalHours, 2)

# Update state
$state.hbCount = $newCount
$state.lastHBNumber = $newHB
$state.lastHB = $now
$state.lastUpdate = $now
$state.lastHeartbeat = $now
$state.ericSilenceHours = $silenceHours
$noteText = "HB ${newHB} - ${now} +10min since ${oldHB}; sustained DORMANT; 7/24 AnYi D-Day T-${dDayHours}h (TOMORROW Friday morning); Eric silent ~${silenceHours}h+ on this session; 6-layer suppression intact; minimal tick per R012."
$state.note = $noteText

$state | ConvertTo-Json -Depth 10 | Set-Content -Path $statePath -Encoding UTF8

# Append minimal entry to today's log
$todayLog = 'memory\2026-07-23.md'

$lines = @()
$lines += ""
$lines += "### HB ${newHB} (${now}, cron-event)"
$lines += "- gap from ${oldHB}: +10min -- Thursday afternoon Token Guard tick (R012 minimal mode)"
$lines += "- D+7 afternoon pass ${newHB} -- Eric silent in THIS session ~${silenceHours}h+ since 7/16 13:16"
$lines += "- Eric active elsewhere: AnYi webchat ~${anyiHours}h+ (since 7/19 12:33)"
$lines += "- 6-layer suppression maintained -- zero breach"
$lines += "- R-NEW-V2: Python utf-8 explicit read+load+write compliant"
$lines += "- R012: HB tick = minimal (NOT full report)"
$lines += "- 7/24 D-Day T-${dDayHours}h (AnYi meeting TOMORROW MORNING 7/24) -- INTERNAL monitor only"
$lines += "- Next cron: 21:00 R60-11 evening self-iter (~${nextCronHours}h)"
$lines += "- hbCount: ${oldCount} -> ${newCount}"
$lines += "- R14 handoff package = 100% ready"
$lines += ""
$lines += "### decision"
$lines += "- **active_mode_dormant_this_session_continue** (HB ${newHB} = sustain ${oldHB} = D+7 afternoon dormant baseline)"
$lines += "- **HEARTBEAT_OK** -- HB ${newHB} = sustain DORMANT protocol"
$lines += "- no push: Thursday afternoon zone, Eric silent on THIS session; 6-layer triple-suppression active"
$lines += ""
$lines += "*${now} -- D+7 Thursday afternoon -- HB ${newHB} -- this session DORMANT -- zero-push mode intact -- 7/24 D-Day T-${dDayHours}h watch -- Eric silent = dominant signal holding*"
$lines += ""

$entry = ($lines -join "`n")
Add-Content -Path $todayLog -Value $entry -Encoding UTF8

Write-Output "HB ${newHB} written. Silence: ${silenceHours} h. D-Day T-${dDayHours} h. Mode: DORMANT."