$ts = (Get-Date).ToString('yyyy-MM-ddTHH:mm:sszzz')
$path = 'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'
$json = Get-Content $path -Raw | ConvertFrom-Json
$json.hbCount = 3581
$json.lastHbTime = $ts
$json.last_update_epoch = [int][double]::Parse((Get-Date -UFormat %s))
$json.notes = 'HB #3581 Thu 13:54 weekday-afternoon. cron DORMANT sustained. No new signal. Stay silent.'
$json.last_hb = @{n=3581; ts=$ts}
$tmp = "$path.tmp"
$json | ConvertTo-Json -Depth 10 | Set-Content -Encoding UTF8 $tmp
Move-Item -Force $tmp $path
Write-Output ("OK hbCount=" + $json.hbCount + " ts=" + $ts)
