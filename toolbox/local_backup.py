#!/usr/bin/env python3
"""
B166ER Local Backup Script
Backup key workspace files to C:\\B166ER-Backup\\
"""

import os
import shutil
import json
from datetime import datetime
from pathlib import Path

BACKUP_ROOT = Path("C:/B166ER-Backup")
WORKSPACE = Path("D:/B166ER-OpenClaw/workspace")

# Key files/dirs to backup (relative to workspace)
KEY_ITEMS = [
    "SOUL.md",
    "USER.md",
    "IDENTITY.md",
    "AGENTS.md",
    "TOOLS.md",
    "MEMORY.md",
    "memory/",
    "anyi-ops-kb/",
    "skills/",
    "toolbox/",
]

def get_dir_size(path):
    """Get directory size in MB"""
    total = 0
    if path.is_file():
        return path.stat().st_size / (1024*1024)
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = Path(dirpath) / f
            try:
                total += fp.stat().st_size
            except:
                pass
    return total / (1024*1024)

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    backup_dir = BACKUP_ROOT / today
    backup_dir.mkdir(parents=True, exist_ok=True)

    report = []
    report.append(f"# B166ER 本地备份报告")
    report.append(f"**时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"**备份目录**: `{backup_dir}`")
    report.append("")
    report.append("## 备份项目")
    report.append("")

    total_size = 0
    for item in KEY_ITEMS:
        src = WORKSPACE / item
        dst = backup_dir / item

        if not src.exists():
            report.append(f"- ~~{item}~~ (不存在，跳过)")
            continue

        # Create parent dirs
        dst.parent.mkdir(parents=True, exist_ok=True)

        if src.is_dir():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            sz = get_dir_size(src)
        else:
            shutil.copy2(src, dst)
            sz = src.stat().st_size / (1024*1024)

        total_size += sz
        report.append(f"- {item} ({sz:.2f} MB)")

    report.append("")
    report.append(f"**总大小**: {total_size:.2f} MB")
    report.append("")

    # Write report
    report_text = "\n".join(report)
    report_path = backup_dir / "backup_report.md"
    report_path.write_text(report_text, encoding="utf-8")

    # Also write to /tmp for Obsidian push
    tmp_path = Path(f"/tmp/local-backup-{today}.md")
    tmp_path.write_text(report_text, encoding="utf-8")

    print(report_text)
    print(f"\n[OK] Backup complete. Report: {report_path}")
    print(f"[OK] Temp file: {tmp_path}")
    print(f"[OK] Size: {total_size:.2f} MB")

    return total_size

if __name__ == "__main__":
    size = main()
