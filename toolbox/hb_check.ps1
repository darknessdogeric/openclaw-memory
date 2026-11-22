Get-ChildItem 'D:\B166ER-OpenClaw\workspace\memory\*.md' -ErrorAction SilentlyContinue |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First 5 |
  ForEach-Object { Write-Host ($_.Name + '  ' + $_.LastWriteTime.ToString('yyyy-MM-dd HH:mm')) }
