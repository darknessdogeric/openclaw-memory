# state.json update - use hashtable to avoid NoteProperty read-only issues
$statePath = 'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'
$raw = Get-Content $statePath -Raw -Encoding UTF8
$obj = $raw | ConvertFrom-Json

# Build a fresh ordered hashtable preserving original keys/values, override the ones we want
$new = [ordered]@{}
foreach ($p in $obj.PSObject.Properties) {
    $new[$p.Name] = $p.Value
}

# Update B166ER-managed fields (do NOT touch gateway-managed hbCount / nullCount / hbLog)
$new['lastHBContext'] = 'Sun 05:40 late-night-deep-quiet zone. DORMANT held (21st consecutive). nullCount (gateway) 820 sustained. Eric silent ~16d 16h+ on cron AND webchat (full dormant convergence). B166ER-file HB #2192 (file-tracked; gateway hbCount 2235+1 = 2236 for THIS poll).'
$new['milestone'] = 'AnYi D+3 = 2026-08-02 Sun 05:40. B166ER-file HB #2192 (file-tracked). Gateway hbCount 2236 (independent). Eric silent ~16d 16h+ on cron AND webchat (full dormant convergence). Next: 06:49 quiet zone exit / 8/3 Mon Day 6 first full workweek start.'
$new['milestoneStatus'] = 'AnYi D+3 = 2026-08-02 Sun 05:40. B166ER-file HB #2192. Gateway hbCount 2236. Eric silent 16d 16h+ (full dormant convergence).'
$new['lastHB'] = 'B166ER-file HB #2192 at 05:40 / gateway HB #2236 at 05:40'
$new['last_update_epoch'] = [int][double]::Parse((Get-Date -UFormat %s))

# Write with UTF-8 noBOM
$json = $new | ConvertTo-Json -Depth 5
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($statePath, $json, $utf8NoBom)

# Verify
$verify = Get-Content $statePath -Raw -Encoding UTF8 | ConvertFrom-Json
Write-Host 'OK state.json updated. lastHB:' $verify.lastHB
Write-Host 'OK state.json updated. lastHBContext (head):' $verify.lastHBContext.Substring(0, [Math]::Min(80, $verify.lastHBContext.Length))