$backupDir = "C:\B166ER-Backup\2026-08-30"
New-Item -ItemType Directory -Force -Path $backupDir | Out-Null

# Root files
Copy-Item -Path "D:\B166ER-OpenClaw\workspace\SOUL.md" -Destination $backupDir -Force
Copy-Item -Path "D:\B166ER-OpenClaw\workspace\IDENTITY.md" -Destination $backupDir -Force
Copy-Item -Path "D:\B166ER-OpenClaw\workspace\USER.md" -Destination $backupDir -Force
Copy-Item -Path "D:\B166ER-OpenClaw\workspace\MEMORY.md" -Destination $backupDir -Force
Copy-Item -Path "D:\B166ER-OpenClaw\workspace\TOOLS.md" -Destination $backupDir -Force
Copy-Item -Path "D:\B166ER-OpenClaw\workspace\HEARTBEAT.md" -Destination $backupDir -Force

# Directories
Copy-Item -Path "D:\B166ER-OpenClaw\workspace\memory" -Destination $backupDir -Recurse -Force
Copy-Item -Path "D:\B166ER-OpenClaw\workspace\anyi-ops-kb" -Destination $backupDir -Recurse -Force
Copy-Item -Path "D:\B166ER-OpenClaw\workspace\.self-improving" -Destination $backupDir -Recurse -Force

# Get size
$size = (Get-ChildItem -Path $backupDir -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB
Write-Host "Backup completed. Size: $([math]::Round($size, 2)) MB"
