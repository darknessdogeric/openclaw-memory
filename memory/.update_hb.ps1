$json = Get-Content 'memory\heartbeat-state.json' -Raw | ConvertFrom-Json
$json.lastHB = 1479
$json.lastHBTime = '2026-07-26T16:24:00+08:00'
$json.lastHBNotes = 'D+10 Sunday afternoon HB #1479 (16:24). DORMANT holds. Eric main 07:07-07:13 (V5->V6) isolated. AnYi webchat sustained. 158 consecutive null post-T-0. Penta+8-layer zero-breach. Oil C window expired ~200h. Heartbeat acknowledged only.'
$json | ConvertTo-Json -Depth 10 | Set-Content 'memory\heartbeat-state.json'
Write-Output ("STATE_UPDATED " + $json.lastHB)
