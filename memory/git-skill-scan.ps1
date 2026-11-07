Set-Location "D:\B166ER-openclaw\workspace\skills"
$results = @()
Get-ChildItem | Where-Object { Test-Path (Join-Path $_.FullName ".git") } | ForEach-Object {
    $p = $_.FullName
    $n = $_.Name
    $b = git -C $p rev-parse --abbrev-ref HEAD 2>&1
    $upRef = git -C $p rev-parse --abbrev-ref '@{u}' 2>&1
    $a = git -C $p rev-list --count '@{u}'..HEAD 2>&1
    $be = git -C $p rev-list --count HEAD..'@{u}' 2>&1
    $s = git -C $p status --short 2>&1
    $dirtyCount = 0
    if ($s) { $dirtyCount = $s.Count }
    $line = "$n [$b -> $upRef] ahead=$a behind=$be dirty=$dirtyCount"
    $results += $line
}
$results | Sort-Object | ForEach-Object { Write-Output $_ }
