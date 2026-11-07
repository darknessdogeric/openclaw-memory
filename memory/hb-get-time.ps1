$ts = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ss+00:00')
$epoch = [DateTimeOffset]::Now.ToUnixTimeSeconds()
Write-Host "Current UTC ts: $ts, epoch: $epoch"
