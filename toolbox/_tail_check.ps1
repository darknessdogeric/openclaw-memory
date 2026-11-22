$bytes = [System.IO.File]::ReadAllBytes('D:\B166ER-OpenClaw\workspace\HEARTBEAT.md')
Write-Host ('File size: {0} bytes' -f $bytes.Length)
Write-Host 'Last 200 bytes hex:'
$start = [Math]::Max(0, $bytes.Length - 200)
for ($i = $start; $i -lt $bytes.Length; $i++) {
    $b = $bytes[$i]
    $hex = '{0:X2}' -f $b
    $c = if ($b -ge 32 -and $b -lt 127) { [char]$b } else { '.' }
    Write-Host ("{0:X2} ({0}) {1}" -f $b, $c)
}