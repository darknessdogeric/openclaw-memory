#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""快速扫描: 只看用户文件位置, 跳过系统目录"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path

# 只看真正可能有 Eric 内容的目录
TARGETS = [
    r"C:\Users\ericz\Desktop",
    r"C:\Users\ericz\Documents",
    r"C:\Users\ericz\Downloads",
    r"C:\Users\ericz\Music",
    r"C:\Users\ericz\Pictures",
    r"C:\Users\ericz\Videos",
    r"C:\Users\ericz\Favorites",
    r"C:\Users\ericz\Links",
    r"C:\Users\ericz\Contacts",
    r"D:\B166ER-OpenClaw",
    r"D:\张实项目总控",
    r"D:\B166ER-Backup",
]


def quick_stat(path: Path) -> dict:
    """快速统计 .md/.docx/.pdf/.xlsx 数"""
    if not path.exists():
        return None
    stats = {'md': 0, 'docx': 0, 'doc': 0, 'pdf': 0, 'xlsx': 0, 'csv': 0, 'pptx': 0, 'audio': 0, 'video': 0, 'images': 0, 'size': 0, 'files': 0}
    try:
        for f in path.rglob("*"):
            if f.is_file():
                stats['files'] += 1
                try:
                    stats['size'] += f.stat().st_size
                except Exception:
                    pass
                ext = f.suffix.lower()
                if ext == '.md':
                    stats['md'] += 1
                elif ext == '.docx':
                    stats['docx'] += 1
                elif ext == '.doc':
                    stats['doc'] += 1
                elif ext == '.pdf':
                    stats['pdf'] += 1
                elif ext in ('.xlsx', '.xls'):
                    stats['xlsx'] += 1
                elif ext == '.csv':
                    stats['csv'] += 1
                elif ext in ('.pptx', '.ppt'):
                    stats['pptx'] += 1
                elif ext in ('.mp3', '.wav', '.flac', '.m4a'):
                    stats['audio'] += 1
                elif ext in ('.mp4', '.mov', '.avi', '.mkv'):
                    stats['video'] += 1
                elif ext in ('.png', '.jpg', '.jpeg', '.gif', '.webp'):
                    stats['images'] += 1
    except Exception as e:
        stats['error'] = str(e)
    return stats


def main():
    print("=" * 80)
    print("快速扫描: 用户文件位置 + D 盘根")
    print("=" * 80)

    for p in TARGETS:
        path = Path(p)
        if not path.exists():
            print(f"  ✗ {p} (NOT EXIST)")
            continue
        s = quick_stat(path)
        if s is None:
            continue
        size_mb = s['size'] / 1024 / 1024
        print(f"  ✓ {p}")
        print(f"      files:{s['files']:6d}  md:{s['md']:5d}  docx:{s['docx']:4d}  pdf:{s['pdf']:3d}  xlsx:{s['xlsx']:3d}  pptx:{s['pptx']:3d}  audio:{s['audio']:4d}  images:{s['images']:5d}  size:{size_mb:7.0f}MB")

    # 找 D 盘根其他位置
    print("\nD:\\ 根其他目录:")
    d_root = Path("D:\\")
    if d_root.exists():
        for d in d_root.iterdir():
            if d.is_dir() and d.name not in ('$RECYCLE.BIN', 'System Volume Information', 'B166ER-OpenClaw'):
                s = quick_stat(d)
                if s and s['files'] > 0:
                    print(f"  {d.name:50s}  files:{s['files']:6d}  md:{s['md']:4d}  size:{s['size']/1024/1024:6.0f}MB")

    # 找 C 盘根其他位置
    print("\nC:\\ 根其他目录:")
    c_root = Path("C:\\")
    if c_root.exists():
        for d in c_root.iterdir():
            if d.is_dir() and d.name not in ('$RECYCLE.BIN', 'System Volume Information', 'Windows', 'Program Files', 'Program Files (x86)', 'ProgramData', 'Users', 'PerfLogs', 'Recovery'):
                s = quick_stat(d)
                if s and s['files'] > 0:
                    print(f"  {d.name:50s}  files:{s['files']:6d}  md:{s['md']:4d}  size:{s['size']/1024/1024:6.0f}MB")


if __name__ == "__main__":
    main()
