$path = 'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'
$state = Get-Content $path -Raw -Encoding UTF8 | ConvertFrom-Json
$state.post_t0_null_count = 1720
$state.last_hb = @{ n = 3152; ts = '2026-08-13T19:02:00+08:00' }
$state.last_check = '2026-08-13T19:02:00+08:00'
$state.note = 'HB #3152; Eric webchat idle 252min (14:50 Panzhihua v6); workday-PM-quiet-active; DORMANT'
$json = $state | ConvertTo-Json -Depth 10
[System.IO.File]::WriteAllText($path, $json, [System.Text.UTF8Encoding]::new($false))
Write-Host ('state.json fixed: hbCount=' + $state.hbCount + ' nullCount=' + $state.nullCount + ' post_t0_null_count=' + $state.post_t0_null_count)
