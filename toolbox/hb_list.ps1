Get-ChildItem 'D:\B166ER-OpenClaw\workspace\memory\2026-08-*.md' -ErrorAction SilentlyContinue | Sort-Object Name -Descending | Select-Object -First 5 | ForEach-Object { Write-Output $_.Name }
