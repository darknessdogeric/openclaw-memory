# File Manager Skill

## Metadata
- **Name**: file-manager
- **Version**: 1.0.0
- **Author**: OpenClaw
- **Description**: Advanced file management operations

## Requirements
- None (uses system commands)

## Configuration
```yaml
# ~/.openclaw/skills/file-manager/config.yaml
default_path: ~/Documents
backup_path: ~/Backups
auto_backup: true
```

## Usage
```bash
# Organize files by date
organize_by_date(path="~/Downloads")

# Find duplicate files
find_duplicates(path="~/Documents")

# Bulk rename
bulk_rename(pattern="*.txt", prefix="doc_")

# Sync directories
sync_directories(source="~/Docs", target="~/Backup/Docs")
```

## Tools
- organize_by_date: Organize files into date folders
- find_duplicates: Find and list duplicate files
- bulk_rename: Rename files in batch
- sync_directories: Sync two directories
- calculate_hash: Calculate file hash (MD5/SHA256)
