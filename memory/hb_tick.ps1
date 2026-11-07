$path = 'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'
$tmp  = $path + '.tmp'
$now  = (Get-Date).ToString('yyyy-MM-ddTHH:mm:sszzz')

$s = Get-Content $path -Raw | ConvertFrom-Json
$s.hbCount   = $s.hbCount + 1
$s.last_tick = $now
$s.lastHBs   = @(@{ ts = $now; hb = $s.hbCount })

$s | ConvertTo-Json | Set-Content -Encoding utf8 $tmp
Move-Item -Force $tmp $path

Write-Host ("HB #" + $s.hbCount + " atomic-tick OK @ " + $now)