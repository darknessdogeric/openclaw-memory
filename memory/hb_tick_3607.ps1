$statePath = 'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'
$tmpPath = $statePath + '.tmp'
$now = (Get-Date).ToString('yyyy-MM-ddTHH:mm:sszzz')
$hb = 3607

$obj = [ordered]@{
  lastHbTime = $now
  posture = 'DORMANT'
  last_hb = @{ n = $hb; ts = $now }
  session = 'cron:315657b9-fc80-4b94-a853-404e3955f7a0'
  lastDecision = 'HEARTBEAT_OK'
  r66_check = 'aligned; no new Eric input; same posture +1 hb cycle'
  r69_silence = 'Expires 2026-08-30 Sun; 10 calendar days remain'
  hbCount = $hb
  notes = "HB #$hb Thu 19:48. +5min from HB #3606. Eric idle ~47h+. R69 T-10d (8/30 Sun). weekday-evening quiet zone active. No state change. Stay silent."
  workday_zone = 'evening-quiet'
  zone = 'evening-quiet'
  anyi_day = 28
  cronSession = 'DORMANT'
}
$json = $obj | ConvertTo-Json -Depth 5
Set-Content -Path $tmpPath -Value $json -Encoding utf8
Move-Item -Force $tmpPath $statePath
Write-Host "HB #$hb tick OK"