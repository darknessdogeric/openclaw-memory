$statePath = 'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'
$state = Get-Content $statePath -Raw | ConvertFrom-Json
$state.hbCount = 3420
$state.nullCount = 1968
$state.post_t0_null_count = 1968
$state.lastHB = '2026-08-16T16:37:00+08:00'
$state.ts = '2026-08-16T16:37:00+08:00'
$state.last_update_epoch = [int][double]::Parse((Get-Date -UFormat %s))
$noteText = 'Sun weekend-afternoon-pre-quiet-zone +5min from 3419, AnYi D+24d Sun (weekend rest), 24-layer suppression holds, no new Eric input, remain dormant, no push, R281 pending, R69 day24 active until 8/30'
$state.notes = @{ hb_3420 = $noteText }
$json = $state | ConvertTo-Json -Depth 10
Set-Content -Path $statePath -Value $json -Encoding UTF8
Write-Host "Updated heartbeat-state.json: hbCount=3420 nullCount=1968"