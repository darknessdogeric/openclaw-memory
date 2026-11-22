Write-Host "Starting..."
$content = Get-Content 'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md' -Raw
$matches = [regex]::Matches($content, '(?m)^## HB #(\d+)')
Write-Host "Found matches: $($matches.Count)"
if ($matches.Count -gt 0) {
    $lastMatch = $matches[$matches.Count - 1]
    Write-Host "Latest HB number: $($lastMatch.Groups[1].Value)"
}
Write-Host "Done."