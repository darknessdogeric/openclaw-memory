$skillsDir = "D:\B166ER-openclaw\workspace\skills"
Get-ChildItem -Directory -Force $skillsDir | Where-Object { Test-Path (Join-Path $_.FullName ".git") } | ForEach-Object {
    $name = $_.Name
    Push-Location $_.FullName
    $branch = git branch --show-current 2>&1
    $ahead = git rev-list --count '@{u}..HEAD' 2>&1
    $behind = git rev-list --count 'HEAD..@{u}' 2>&1
    $last = git log -1 --format="%h %ci %s" 2>&1
    $status = git status --porcelain 2>&1
    Write-Host "=== $name ==="
    Write-Host "branch: $branch | ahead: $ahead | behind: $behind"
    Write-Host "last: $last"
    if ($status) {
        $status | Select-Object -First 6
    } else {
        Write-Host "(clean)"
    }
    Pop-Location
}
