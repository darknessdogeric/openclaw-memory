$f = 'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md'
$content = [System.IO.File]::ReadAllText($f, [System.Text.Encoding]::UTF8)

# Find all HB #2xxx occurrences
$regex = [regex]'(HB #2\d{3})'
$matches = $regex.Matches($content)
Write-Host 'Total HB matches:' $matches.Count
Write-Host 'Last 10 HB entries (by position):'
for ($i = [Math]::Max(0, $matches.Count - 10); $i -lt $matches.Count; $i++) {
    $m = $matches[$i]
    $lineStart = $content.LastIndexOf("`n", $m.Index) + 1
    $lineEnd = $content.IndexOf("`n", $m.Index)
    if ($lineEnd -lt 0) { $lineEnd = $content.Length }
    $line = $content.Substring($lineStart, $lineEnd - $lineStart)
    Write-Host ("[" + $i + "] pos=" + $m.Index + ": " + $line)
}

# Find the HB #2192 marker and the time after it
$idx = $content.LastIndexOf('HB #2192')
Write-Host '---'
Write-Host 'Last HB #2192 at char index:' $idx
$entry = $content.Substring($idx, [Math]::Min(800, $content.Length - $idx))
Write-Host 'First 800 chars:'
Write-Host $entry