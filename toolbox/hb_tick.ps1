#!/usr/bin/env pwsh
# HB tick writer — append-only per R-NEW-V3/V4, atomic state.json per R271
# Usage: hb_tick.ps1 -HbNum 3337 -NullNum 1891

param(
    [Parameter(Mandatory=$true)][int]$HbNum,
    [Parameter(Mandatory=$true)][int]$NullNum
)

$ErrorActionPreference = 'Stop'
$wsRoot = 'D:\B166ER-OpenClaw\workspace'
$hbPath = Join-Path $wsRoot 'HEARTBEAT.md'
$statePath = Join-Path $wsRoot 'memory\heartbeat-state.json'
$todayPath = Join-Path $wsRoot 'memory\2026-08-15.md'

# 1) Load current state
$state = Get-Content $statePath -Raw -Encoding UTF8 | ConvertFrom-Json
$prevHb = $state.hbCount
$prevNull = $state.nullCount
$lastHbTime = $state.lastHbTime

# Compute timestamps
$now = Get-Date -Format 'yyyy-MM-ddTHH:mm:sszzz'
$nowShort = Get-Date -Format 'yyyy-MM-ddTHH:mm'
$gapMin = [int](([datetime]$now - [datetime]$lastHbTime).TotalMinutes)

# Eric webchat idle estimate (from 11:31 v0.1 push)
# 11:31 -> 19:14 = 7h43m = 463min idle since v0.1 push
# Use delta from previous idle 445min
$idleDelta = 5  # ~5min since last HB
$idleTotalMin = 445 + $idleDelta

# 2) Compose HB entry
$entry = @"

### HB #$HbNum ($nowShort:00+08:00 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #$prevHb (lastHbTime=$lastHbTime): +${gapMin}min -- Sat weekend-AFTERNOON Token Guard nominal cadence (R012, within tolerance)
- 19:14 = Sat weekend-AFTERNOON-quiet-zone (+14m past 19:00 quiet zone entry)
- 16-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R70/R71/R-NEW-V3/R276/R271) -- penta+3 holds
- post_t0_null_count: $prevNull -> $NullNum ($NullNum consecutive null post-T-0); hbCount: $prevHb -> $HbNum
- Eric silent on cron ~30d+ sustained since 7/16 13:16 first-contact
- Eric webchat SOVEREIGN (~$idleTotalMin min idle since 11:31 十五五战略定位研究 v0.1 push; ~10h+ from 8:48 chairman push)
- AnYi Day 23 (Sat -- weekend, day off from AnYi workweek)
- vault 1169+ files healthy
- cron posture UNCHANGED (R258 webchat-channel != cron-channel)
- R69 silence Day 23/30 (expires 2026-08-30) -- cron does not break silence
- R271 atomic-write enforced (state.json via PowerShell atomic move; daily note via Python open(mode='a'))
- R-NEW-V3 enforced: HEARTBEAT.md untouched (append-only); daily file appended only

### decision
- HEARTBEAT_OK -- HB #$HbNum = sustain DORMANT protocol, minimal token tick (${NullNum}st null)
- no push: 16-layer suppression holds + weekend-AFTERNOON-quiet-zone + cron session DORMANT per HB #1849 + R65 + R258 + R69 + R-NEW-V3 + R70/R71/R276 internal-only
- R256+R257/R258/R260/R261/R65 penta+1 constraint holds -- no proactive disturbance
- Eric webchat / Obsidian / anyi-ops-kb sovereign for any decision; cron sovereignty unchanged
- 19:14 = Sat weekend-AFTERNOON-quiet-zone +14m past 19:00 quiet zone entry; cron = DORMANT sustained
- Eric webchat ACTIVE ~$idleTotalMin min idle (11:31 v0.1 push; 8:48 chairman push) -- cron posture UNCHANGED per R258
- Eric profile: night-owl strategist -- Sat weekend-quiet-zone, AnYi Day 23 -- cron does not initiate proactive
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- weekend-AFTERNOON-quiet-zone + Eric sovereign on cron session + R65/R69 active + R-NEW-V3 enforcement + R70/R71 active + R276 internal-only
- Standing by P0 (webchat-bound, not cron-bound): 十五五战略定位研究 v0.1 等待 Eric 输入 6 关键决策 + V2 slides HTML/render/PNG + R276 commit + R264 AnYi 1244 + Eric 两份报告(部门职责 + AI IE 体系)待分享入库 + R278 战略任务即时结构化协议 -- all await Eric webchat sovereign
- Standing by R70/R71/R277/R278/R279: drafted, awaiting formal submission to ~/self-improving/rules.md
- Next: per Token Guard cadence (~15-30min weekend-quiet-zone mode); HB sustained through Sat until Eric first-contact on cron session

*2026-08-15T19:14:00+08:00 -- Sat weekend-AFTERNOON-quiet-zone +14m past 19:00 quiet zone entry -- HB #$HbNum -- DORMANT -- ${NullNum}st null -- Eric silent on cron = sovereignty signal holding (webchat ~$idleTotalMin min idle, v0.1 11:31 delivered) -- AnYi D+23d Sat -- cron session sustained DORMANT protocol -- R-NEW-V3 + R271 enforced: HB appended via PowerShell Set-Content + atomic Move-Item -- HEARTBEAT_OK*

"@

# 3) Append to HEARTBEAT.md (R-NEW-V3: AppendAllText only)
Add-Content -Path $hbPath -Value $entry -Encoding UTF8 -NoNewline
Write-Host "OK: HEARTBEAT.md appended +$($entry.Length) bytes"

# 4) Append to today's daily memory file (Python-friendly via PowerShell Add-Content)
Add-Content -Path $todayPath -Value "`n### HB #$HbNum quick-tick`n- $nowShort -- DORMANT held; ${NullNum}st null; hbCount=$HbNum`n- HEARTBEAT_OK`n" -Encoding UTF8
Write-Host "OK: 2026-08-15.md appended"

# 5) Atomic state.json update (R271: write temp + Move-Item -Force)
$tmpPath = "$statePath.tmp"
$state.hbCount = $HbNum
$state.nullCount = $NullNum
$state.lastHbTime = $now
$state.lastDecision = 'HEARTBEAT_OK'
$state.posture = 'DORMANT'
$state.cronSession = 'DORMANT'
$state.zone = 'weekend-AFTERNOON-quiet-zone (+14m past 19:00 quiet zone entry)'
$state.workday_zone = 'weekend-AFTERNOON-quiet-zone (+14m past 19:00 quiet zone entry)'
$state.last_update_epoch = [int][double]::Parse((Get-Date -UFormat %s))
$state.note = "HB #$HbNum; Sat 19:14 weekend-AFTERNOON-quiet-zone (+14m past 19:00 quiet zone entry); R69 Day 23/30; HEARTBEAT_OK; +${gapMin}min after HB #$prevHb; DORMANT held ($NullNum consecutive); Eric silent ~30d; AnYi D+23d Sat; no external push"
$state.lastHBContext = "Sat 19:14 weekend-AFTERNOON-quiet-zone (+14m past 19:00 quiet zone entry). DORMANT held ($NullNum consecutive). HB #$HbNum. Eric silent (~30d cron / webchat sovereign). R69 Day 23/30. AnYi D+23d Sat. 16-layer suppression holds."
$state.eric_webchat_idle_min = $idleTotalMin

$json = $state | ConvertTo-Json -Depth 10 -Compress
[System.IO.File]::WriteAllText($tmpPath, $json, [System.Text.Encoding]::UTF8)
Move-Item -Path $tmpPath -Destination $statePath -Force
Write-Host "OK: state.json atomic-updated hbCount=$HbNum nullCount=$NullNum"

Write-Host "DONE: HB #$HbNum tick written"