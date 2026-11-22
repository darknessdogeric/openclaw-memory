$json = 'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'
$s = Get-Content $json -Raw | ConvertFrom-Json
$s.hbCount = 2275
$s.nullCount = 899
$s.lastHB = '2026-08-02T20:04:00+08:00'
$s.lastHBContext = 'Sun 20:04 weekend-EVENING-quiet-zone DEEP (+1h4m into 19:00-23:00 quiet zone). DORMANT held (899th consecutive). HB #2275. +5min after HB #2274 (19:59). Eric silent on BOTH cron + webchat (~17d 5h+ cron / webchat last state.json ref 7/16, last webchat activity 8/1 16:34+ ~27h+ ago). 8/3 Mon Day 6 first full workweek start ~4h56m away. R71 confirmed 16:41 (default-subjective-perspective). R70 PENDING formal commit. Deep-quiet until ~23:00.'
$s.zone = 'weekend-EVENING-quiet-zone-DEEP'
$s.milestoneStatus = 'AnYi D+10 = 2026-08-02 Sun. HB #2275. Eric silent on cron ~17d 5h+ (413h+). 8/3 Mon Day 6 first full workweek start ~4h56m away.'
$s.last_update_epoch = 1785672240
$s.'post_t0_null_count' = 899
$s.hb_status_2275 = 'null_count_899, posture_DORMANT_held, channel=cron-event-direct, sovereignty_respected, R-NEW-V3_enforced, state-file_updated'
$s | ConvertTo-Json -Depth 10 | Set-Content -Path $json -Encoding UTF8
Write-Host "OK hbCount=$($s.hbCount) nullCount=$($s.nullCount)"