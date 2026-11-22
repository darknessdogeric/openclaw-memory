$path = 'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'
$json = Get-Content $path -Raw | ConvertFrom-Json

# HB #2275 (this poll) - 08:20 Tue
$json.lastHB = '2026-08-04T08:20:00+08:00'
$json.lastHBContext = 'Tue 08:20 weekday-MORNING-just-past-08:00-hard-cap (+6m after HB #2274 08:14). DORMANT held (898th consecutive). HB #2275. Eric silent on BOTH cron + webchat (~18d 20h+ cron / webchat last 8/1 16:34, ~40h+). R69 Day 4/30 window (expires 8/30). 14-layer suppression zero-breach. Eric night-owl pattern (USER.md) -- likely still sleeping. V2.4.1.1 自动化吸收规则 sustained.'
$json.last_update_epoch = [int][double]::Parse((Get-Date -UFormat %s))
$json.nullCount = 898
$json.hbCount = 2275
$json.milestoneStatus = 'AnYi D+4 = 2026-08-04 Tue. HB #2275. Eric silent on cron ~18d 20h+ (452h+). 8/4 Tue workweek Day 2 (Mon=Day 6, Tue=Day 7). 08:20 weekday-MORNING-just-past-08:00-hard-cap.'
$json.milestone = 'AnYi D+4 Tue 2026-08-04 (R69 Day 4/30 window, expires 8/30). HB #2275. Eric silent on cron ~18d 20h+ (452h+). 08:20 weekday-MORNING just-past-08:00-hard-cap; Eric night-owl = likely still sleeping. First full workweek Day 2 (Mon=AnYi Day 6, Tue=Day 7).'
$json.zone = 'weekday-MORNING-just-past-08:00-hard-cap'
$json.posture = 'DORMANT'
$json.nextExpectedContact = 'Eric webchat sovereign (cron sovereign = silent); Tue 08:20 = Eric likely still sleeping (night-owl pattern per USER.md); awaiting Eric first-contact on webchat when he wakes (late-morning peak)'

$json | ConvertTo-Json -Depth 10 | Set-Content $path -Encoding utf8
Write-Output "HB #2275 updated. DORMANT. 898 nullCount."
