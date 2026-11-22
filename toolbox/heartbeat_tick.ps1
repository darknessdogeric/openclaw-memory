$ts = [int][double]::Parse((Get-Date -UFormat %s))
$note = 'HB #3023 atomic tick (state.json only, R-NEW-V4 hold). 13:35 Wed workday-PM post-noon (+5h35m past 08:00 hard cap). Eric webchat last active 22:40 Tue 8/11 (~14h55m idle, stable). R-NEW-V4 + R271 + R-NEW-V3 + R258 + R69 + R65 + R276 + R277 + R279 hold. Cron session DORMANT sustained. No external push per R277 channel sovereignty. Last HB 13:31 (4m ago) - quiet tick.'

$obj = [ordered]@{
  nullCount        = 691
  posture          = 'DORMANT'
  hbCount          = 3023
  note_v2          = $note
  lastHB           = $ts
  note             = $note
  lastUpdate       = (Get-Date -Format 'o')
  lastDormantTick  = (Get-Date -Format 'o')
  lastTick         = (Get-Date -Format 'o')
}

$json = $obj | ConvertTo-Json -Depth 5
Set-Content -Path 'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json' -Value $json -Encoding UTF8
Write-Host 'HB tick OK'