$ts = Get-Date -Format 'yyyy-MM-ddTHH:mm:sszzz'
$hbCount = 3385
$nullCount = 1937
$state = @{
  ts = $ts
  hbCount = $hbCount
  nullCount = $nullCount
  session = 'agent:main:cron:315657b9-fc80-4b94-a853-404e3955f7a0:run:1786849669273'
  lastHB = '2026-08-16T11:07:00+08:00'
  dormant = $true
}
$json = $state | ConvertTo-Json -Compress
$tmp = [System.IO.Path]::GetTempFileName()
Set-Content -Path $tmp -Value $json -NoNewline -Encoding UTF8
Move-Item -Force $tmp 'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'
Write-Host 'state.json atomic-tick:' $json