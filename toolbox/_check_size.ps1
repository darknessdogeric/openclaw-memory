$dirs = @('memory','toolbox','skills','obsidian-vault','self-improving')
foreach ($name in $dirs) {
    $path = Join-Path 'D:\B166ER-OpenClaw\workspace' $name
    if (Test-Path $path) {
        $size = (Get-ChildItem $path -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
        Write-Host ("{0,-20} {1,12:N2} MB" -f $name, ($size/1MB))
    }
}
