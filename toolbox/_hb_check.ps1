$f='D:\B166ER-OpenClaw\workspace\memory\2026-07-16.md'
if (Test-Path $f) {
    Get-Item $f | Select-Object Length, LastWriteTime | Format-List
} else {
    'NOT_FOUND'
}