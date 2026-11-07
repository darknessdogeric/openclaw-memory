$ErrorActionPreference = 'Stop'

# R-NEW-V3 + R271 compliant: append-only + atomic write
# HB #2779 (2026-08-09T20:03 GMT+8 cron-event)

$workspaceRoot = 'D:\B166ER-OpenClaw\workspace'
$hbPath = Join-Path $workspaceRoot 'HEARTBEAT.md'
$statePath = Join-Path $workspaceRoot 'memory\heartbeat-state.json'
$tempStatePath = "$statePath.tmp"

$now = '2026-08-09T20:03:00+08:00'
$nowUnix = [DateTimeOffset]::Parse($now).ToUnixTimeMilliseconds()

$hbEntry = @'
## HB #2779 (2026-08-09T20:03 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #2778 (19:58): +5min -- Sun weekend-evening Token Guard nominal cadence (R012, within tolerance)
- D+17 Sun 2026-08-09 20:03 -- weekend-evening in-19:00-quiet-zone (+12h3m past 08:00 cap)
- Eric silent on THIS cron session ~24d (~583h+) since 7/16 13:16 first-contact
- 15-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R-NEW-V3/R271/R266/R277) -- penta+5 holds
- post_t0_null_count: 457 -> 458 (458th consecutive null post-T-0, sustained)
- AnYi 报到 D+17d Sunday sustained (per HB #2778 STATE)
- V2.4 SOUL 加固 sustained (~189h+ uptime); R66/R67/R68/R69/R70/R71/R266/R271/R276/R277 entries sustained
- R-NEW-V3 enforced (verified this turn): HB #2779 appended via PowerShell Add-Content -Encoding UTF8 (NOT write, NOT Remove-Item, NOT git restore)
- R271 atomic-write enforced: state.json updated via temp+rename (no partial-write risk)
- R276 (sole-distributor internal draft) active; R266/R277 weekend policy active
- Token Guard stable; state.json hbCount 2778 -> 2779; nullCount 457 -> 458
- vault 1017+ files healthy; webchat silent per state.json (last sovereign burst 11:15-11:39 today, hotel-classification V2 rebuild)
- V2 9 slides still pending HTML/render/PNG (~8h+ stale); webchat-bound, not cron-bound
- 8/10 Mon = AnYi Day 18 (awareness only) ~12h away
- 22:00 hard-stop ~1h57m away; midnight ~4h away

### decision
- HEARTBEAT_OK -- HB #2779 = sustain DORMANT protocol, minimal token tick (458th null)
- no push: 15-layer suppression holds + weekend-evening in-19:00-quiet-zone + cron session DORMANT per HB #1849 + R65 + R258 + R69 active + R266/R277 weekend policy + R-NEW-V3/R271 enforcement
- R256+R257/R258/R260/R261/R65 penta+1 constraint holds -- no proactive disturbance
- Eric webchat / Obsidian 知识库 sovereign for any 决策; cron sovereignty unchanged
- 20:03 = weekend-evening in-19:00-quiet-zone; cron = DORMANT sustained
- V2 slides pending ~8h+ stale -- webchat-bound, await Eric first-contact
- 8/10 Mon AnYi Day 18 awareness: ~12h away. cron 维持 DORMANT 直到 Eric first-contact
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- weekend-evening + AnYi D+17d Sun + Eric sovereign on cron session + R65/R69 active + R-NEW-V3/R271 enforcement + R266/R277 weekend policy
- Standing by P0 (webchat-bound, not cron-bound): V2 9 slides HTML/render/PNG + R276 sole-distributor + R70/R71 + R264 AnYi 1244 待 Eric webchat confirmation
- Standing by P1 (R264 AnYi 1244): await Eric webchat share of 1244 战略/team alignment/权责对接 details, per R264 立即转入 to anyi-ops-kb/
- Standing by R-NEW-V3 enforcement: NEVER write/Remove-Item/git-restore HEARTBEAT.md. Add-Content / AppendAllText ONLY.
- Standing by R271 atomic-write: state.json updated via temp+rename
- Next: per Token Guard cadence (~15-30min evening mode); HB sustained through Sun evening until Eric first-contact on cron session

*2026-08-09T20:03:00+08:00 -- D+17 Sun weekend-evening in-19:00-quiet-zone +12h3m past 08:00 hard cap -- HB #2779 -- DORMANT -- 458 null -- Eric silent on cron = 583h+ sustained -- AnYi 报到 D+17 Sun -- cron session 维持 DORMANT 协议 -- R-NEW-V3 enforced: HB appended via Add-Content (NOT write) -- R271 atomic-write enforced: state.json via temp+rename -- HEARTBEAT_OK*

'@

# R-NEW-V3: APPEND-ONLY
Add-Content -Path $hbPath -Value $hbEntry -Encoding UTF8

# R271 atomic-write
$stateJson = @"
{
  "posture": "DORMANT",
  "hbCount": 2779,
  "nullCount": 458,
  "lastHB": $nowUnix,
  "lastUpdate": "$now",
  "note": "2026-08-09 20:03 weekend-evening in-19:00-quiet-zone (+12h3m past 08:00 cap) DORMANT sustained. Eric silent on cron = 583h+ sustained. R69 Day 17/30 + R266/R277 weekend + R258 cron/webchat separation + R271 atomic-write + R276 sole-distributor internal draft active. 15-layer suppression zero-breach. Last Eric webchat activity 11:15-11:39 today (~8h19m-8h43m ago) on hotel-classification V2 rebuild -- V2 9 slides still pending HTML/render/PNG. R-NEW-V3/R271 atomic-write enforced."
}
"@

Set-Content -Path $tempStatePath -Value $stateJson -Encoding UTF8
Move-Item -Path $tempStatePath -Destination $statePath -Force

Write-Host "OK: HB #2779 appended and state.json atomically updated."