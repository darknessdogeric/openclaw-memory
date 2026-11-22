#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B166ER 每日本地备份脚本
每日 02:00 把关键 workspace 文件本地备份到 C:\\B166ER-Backup\\
"""
import os
import shutil
import datetime
from pathlib import Path
import json

WORKSPACE = Path(r"D:\B166ER-OpenClaw\workspace")
BACKUP_ROOT = Path(r"C:\B166ER-Backup")
TODAY = datetime.datetime.now().strftime("%Y-%m-%d")
BACKUP_DIR = BACKUP_ROOT / TODAY

# 关键备份源（相对 WORKSPACE 或绝对路径）
SOURCES_REL = [
    ("core", "SOUL.md"),
    ("core", "IDENTITY.md"),
    ("core", "AGENTS.md"),
    ("core", "USER.md"),
    ("core", "TOOLS.md"),
    ("core", "MEMORY.md"),
    ("memory", "memory"),
    ("openclaw-cfg", ".openclaw"),
]

def fmt_size(num_bytes: int) -> str:
    if num_bytes < 1024:
        return f"{num_bytes} B"
    elif num_bytes < 1024 ** 2:
        return f"{num_bytes / 1024:.1f} KB"
    elif num_bytes < 1024 ** 3:
        return f"{num_bytes / 1024 ** 2:.1f} MB"
    else:
        return f"{num_bytes / 1024 ** 3:.2f} GB"

def dir_size(p: Path) -> int:
    return sum(f.stat().st_size for f in p.rglob("*") if f.is_file())

def safe_copy(src: Path, dst: Path, ignore_git: bool = True) -> tuple[bool, int, str]:
    """复制文件/目录，返回 (ok, size, error)。ignore_git=True 时跳过 .git 大目录"""
    try:
        if not src.exists():
            return False, 0, "not exist"
        if src.is_file():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            return True, src.stat().st_size, ""
        elif src.is_dir():
            if dst.exists():
                shutil.rmtree(dst)
            ignore_pats = shutil.ignore_patterns(
                "__pycache__", "*.pyc", ".venv", "node_modules",
                "*.tmp", "*.bak", ".chroma_db"
            )
            if ignore_git:
                ignore_pats = shutil.ignore_patterns(
                    "__pycache__", "*.pyc", ".venv", "node_modules",
                    "*.tmp", "*.bak", ".chroma_db", ".git"
                )
            shutil.copytree(src, dst, ignore=ignore_pats)
            total = dir_size(dst)
            return True, total, ""
        else:
            return False, 0, "unsupported type"
    except Exception as e:
        return False, 0, str(e)

def safe_rmtree(p: Path) -> tuple[bool, str]:
    """容错删除，处理权限错误"""
    try:
        shutil.rmtree(p, onerror=lambda *args: None)
        # 再次确认
        if p.exists():
            return False, "still exists"
        return True, ""
    except Exception as e:
        return False, str(e)

def cleanup_old_backups(cutoff_days: int = 14) -> tuple[list, list]:
    """清理超过 N 天的旧备份"""
    cutoff = datetime.datetime.now() - datetime.timedelta(days=cutoff_days)
    removed = []
    errors = []
    if not BACKUP_ROOT.exists():
        return removed, errors
    for old_dir in sorted(BACKUP_ROOT.iterdir()):
        if not old_dir.is_dir():
            continue
        try:
            dir_date = datetime.datetime.strptime(old_dir.name, "%Y-%m-%d")
            if dir_date < cutoff:
                ok, err = safe_rmtree(old_dir)
                if ok:
                    removed.append(old_dir.name)
                else:
                    errors.append((old_dir.name, err))
        except ValueError:
            continue
    return removed, errors

def main():
    BACKUP_ROOT.mkdir(parents=True, exist_ok=True)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    results = []
    total_size = 0

    # 1. 备份 workspace 内核心文件
    for category, rel in SOURCES_REL:
        src_path = (WORKSPACE / rel).resolve()
        dst_path = BACKUP_DIR / category / Path(rel).name
        ok, size, err = safe_copy(src_path, dst_path)
        results.append({
            "category": category,
            "source": str(src_path),
            "destination": str(dst_path),
            "ok": ok,
            "size": size,
            "error": err,
        })
        if ok:
            total_size += size

    # 2. 备份 ~/self-improving/（独立路径）
    self_improving = Path.home() / "self-improving"
    if self_improving.exists():
        dst_path = BACKUP_DIR / "self-improving"
        ok, size, err = safe_copy(self_improving, dst_path)
        results.append({
            "category": "self-improving",
            "source": str(self_improving),
            "destination": str(dst_path),
            "ok": ok,
            "size": size,
            "error": err,
        })
        if ok:
            total_size += size

    # 3. 清理旧备份（先做，避免污染 manifest）
    removed, remove_errors = cleanup_old_backups(14)

    # 4. 写 manifest.json
    manifest = {
        "date": TODAY,
        "started_at": datetime.datetime.now().isoformat(),
        "workspace": str(WORKSPACE),
        "backup_root": str(BACKUP_ROOT),
        "backup_dir": str(BACKUP_DIR),
        "total_size_bytes": total_size,
        "total_size_human": fmt_size(total_size),
        "results": results,
        "summary": {
            "total": len(results),
            "ok": sum(1 for r in results if r["ok"]),
            "failed": sum(1 for r in results if not r["ok"]),
        },
        "cleanup": {
            "removed": removed,
            "errors": remove_errors,
            "retention_days": 14,
        },
    }
    manifest_path = BACKUP_DIR / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    # 5. 输出
    print(f"[OK] 备份完成: {BACKUP_DIR}")
    print(f"  - 总大小: {fmt_size(total_size)}")
    print(f"  - 文件/目录数: {manifest['summary']['total']}")
    print(f"  - 成功: {manifest['summary']['ok']}, 失败: {manifest['summary']['failed']}")
    if removed:
        print(f"  - 已清理 {len(removed)} 个旧备份: {', '.join(removed)}")
    if remove_errors:
        print(f"  - [WARN] {len(remove_errors)} 个旧目录清理失败（文件锁/权限）")
        for d, e in remove_errors[:3]:
            print(f"    - {d}: {e}")

    # 输出 JSON 给外层脚本读
    print("\n---MANIFEST_JSON_START---")
    print(json.dumps(manifest, ensure_ascii=False))
    print("---MANIFEST_JSON_END---")

if __name__ == "__main__":
    main()