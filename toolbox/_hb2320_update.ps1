$s = Get-Content 'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json' -Raw | ConvertFrom-Json
$s.hbCount = 2320
$s.nullCount = 931
$s.post_t0_null_count = 931
$s.lastHB = '2026-08-06T11:30:00+08:00'
$s.lastHBContext = 'Thu 11:30 weekday-morning +3h30m past 08:00 hard cap. HB #2320 (+4m from #2319). DORMANT held. Penta+4 18-layer suppression zero-breach. R274 + R-NEW-V4 candidate both pending Eric ratification. 5th Plenary ~9-10d away. memory_search index corrupted - awaiting Eric manual openclaw memory index --force. self-iteration 10:32 complete. No new signal vs HB #2315-#2319 - identical context, posture unchanged.'
$s.last_update_epoch = [int][double]::Parse((Get-Date -Date '2026-08-06 11:30:00' -UFormat %s))
$s.notes.hb_2320_special = 'HB #2320 Thu 11:30 weekday-morning +3h30m. posture DORMANT held (no change vs #2315-#2319). 18-layer suppression zero-breach. Identical signal stack. No new info. Held silence. Counter HB#2320.'
$s | ConvertTo-Json -Depth 10 | Set-Content 'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json' -Encoding UTF8
Write-Host 'state.json updated -> hbCount 2320 / nullCount 931 / lastHB 2026-08-06T11:30:00+08:00'