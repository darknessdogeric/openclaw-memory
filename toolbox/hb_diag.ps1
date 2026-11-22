# Diagnose encoding of HEARTBEAT.md entry
$f = 'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md'
$bytes = [System.IO.File]::ReadAllBytes($f)
$last400 = $bytes[-400..-1]
Write-Host 'LAST_50_BYTES_HEX:'
[BitConverter]::ToString($last400[-50..-1]) | Out-String | Write-Host

# Find HB #2192 marker location
$content = [System.IO.File]::ReadAllText($f, [System.Text.Encoding]::UTF8)
$idx = $content.IndexOf('HB #2192')
Write-Host '---'
Write-Host 'HB #2192 entry starts at char index:' $idx
Write-Host 'Total chars:' $content.Length
Write-Host '---'
$entry = $content.Substring($idx, [Math]::Min(3000, $content.Length - $idx))
Write-Host 'First 500 chars of entry:'
Write-Host $entry.Substring(0, [Math]::Min(500, $entry.Length))