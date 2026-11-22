$json = 'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'
$s = Get-Content $json -Raw | ConvertFrom-Json
$s | Add-Member -NotePropertyName 'hb_status_2275' -NotePropertyValue 'null_count_899, posture_DORMANT_held, channel=cron-event-direct, sovereignty_respected, R-NEW-V3_enforced, state-file_updated' -Force
$s | ConvertTo-Json -Depth 10 | Set-Content -Path $json -Encoding UTF8
Write-Host "OK hbCount=$($s.hbCount) hb_status_2275 added"