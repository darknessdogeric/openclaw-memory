#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""全盘扫描 v2: 整台电脑 (C:\ + D:\ 根 + 用户目录)"""
import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from collections import defaultdict

# 重点扫的根
SCAN_ROOTS = [
    Path(r"D:\B166ER-OpenClaw"),
    Path(r"D:\张实项目总控"),
    Path("D:\\"),
    Path(r"C:\Users\ericz\Desktop"),
    Path(r"C:\Users\ericz\Documents"),
    Path(r"C:\Users\ericz\OneDrive"),
    Path(r"C:\Users\ericz\Music"),
    Path(r"C:\Users\ericz\Pictures"),
    Path(r"C:\Users\ericz\Videos"),
    Path(r"C:\Users\ericz\Downloads"),
    Path("C:\\Eric"),
    Path("C:\\E盘"),
    Path("D:\\E盘"),
    Path("E:\\"),
    Path("F:\\"),
]

# 已知 Eric 的项目位置（从 MEMORY/IDENTITY 知道）
KNOWN_PATHS = [
    r"C:\Users\ericz\Desktop\张实项目总控",
    r"C:\Users\ericz\Desktop\obsidian",
    r"C:\Users\ericz\Documents",
    r"D:\张实项目总控",
    r"D:\B166ER-OpenClaw",
    r"D:\B166ER-Backup",
    r"E:\Eric",
    r"E:\Eric-Backup",
    r"F:\Eric",
    r"F:\F盘资料",
]

# 必须排除
EXCLUDE = [
    'node_modules', '.git', '.backups', '.openclaw', 'obsidian-vault',
    '.agents', '.clawhub', '.iflow', '.last30days-skill',
    '.playwright-cli', '.self-improving', '.tmp', '.next', '.venv',
    'cache', '__pycache__', '.pytest_cache',
    'Windows', 'Program Files', 'ProgramData', 'Users/Default', '$Recycle.Bin',
    'AppData', 'Recycle.Bin', 'System Volume Information', 'Recovery',
    'Config.Msi', 'Documents and Settings', 'PerfLogs',
    'MSOCache', 'OneDriveTemp',
]


def should_skip(path: Path) -> bool:
    s = str(path).lower()
    for ex in EXCLUDE:
        if ex.lower() in s:
            return True
    return False


def count_files(root: Path, exts=None) -> dict:
    """统计 root 下文件"""
    stats = {'files': 0, 'md': 0, 'pdf': 0, 'docx': 0, 'txt': 0,
             'json': 0, 'images': 0, 'audio': 0, 'video': 0,
             'sop': 0, 'doc': 0, 'xlsx': 0, 'pptx': 0, 'other': 0,
             'total_size': 0}
    if not root.exists():
        return {'error': f'NOT EXIST: {root}'}
    for f in root.rglob("*"):
        if f.is_file():
            if should_skip(f):
                continue
            try:
                size = f.stat().st_size
            except Exception:
                continue
            stats['total_size'] += size
            stats['files'] += 1
            ext = f.suffix.lower()
            if ext == '.md':
                stats['md'] += 1
            elif ext == '.pdf':
                stats['pdf'] += 1
            elif ext in ('.docx',):
                stats['docx'] += 1
            elif ext == '.doc':
                stats['doc'] += 1
            elif ext == '.txt':
                stats['txt'] += 1
            elif ext == '.json':
                stats['json'] += 1
            elif ext in ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.bmp'):
                stats['images'] += 1
            elif ext in ('.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg'):
                stats['audio'] += 1
            elif ext in ('.mp4', '.mov', '.avi', '.mkv', '.webm'):
                stats['video'] += 1
            elif ext in ('.xlsx', '.xls', '.csv'):
                stats['xlsx'] += 1
            elif ext in ('.pptx', '.ppt'):
                stats['pptx'] += 1
            else:
                stats['other'] += 1
    return stats


def main():
    print("=" * 80)
    print("整台电脑扫描 (C: + D:) · 找所有可纳入 vault 的内容")
    print("=" * 80)

    all_dirs = []

    # 1. 已知 Eric 项目位置
    print("\n[1] 已知 Eric 项目位置")
    for p in KNOWN_PATHS:
        path = Path(p)
        if path.exists():
            s = count_files(path)
            if 'error' not in s:
                print(f"  ✓ {p}")
                print(f"      files: {s['files']}  md: {s['md']}  pdf: {s['pdf']}  docx: {s['docx']}  xlsx: {s['xlsx']}  size: {s['total_size']/1024/1024:.0f}MB")
                all_dirs.append((p, s))
            else:
                print(f"  ✗ {p} (NOT EXIST)")
        else:
            print(f"  ✗ {p} (NOT EXIST)")

    # 2. 用户目录顶层
    print("\n[2] C:\\Users\\ericz 顶层目录")
    user_root = Path(r"C:\Users\ericz")
    for d in user_root.iterdir():
        if d.is_dir() and not should_skip(d):
            s = count_files(d)
            if s.get('files', 0) > 5 or s.get('md', 0) > 0:
                print(f"  {d.name:40s}  files:{s['files']:6d}  md:{s['md']:4d}  pdf:{s['pdf']:3d}  docx:{s['docx']:3d}  xlsx:{s['xlsx']:3d}  size:{s['total_size']/1024/1024:6.0f}MB")

    # 3. D:\ 根（除 B166ER-OpenClaw）
    print("\n[3] D:\\ 根目录")
    d_root = Path("D:\\")
    for d in d_root.iterdir():
        if d.is_dir() and not should_skip(d):
            if d.name == 'B166ER-OpenClaw':
                continue
            s = count_files(d)
            print(f"  {d.name:40s}  files:{s.get('files', 0):6d}  md:{s.get('md', 0):4d}  size:{s.get('total_size', 0)/1024/1024:6.0f}MB")

    # 4. C:\ 根（除系统）
    print("\n[4] C:\\ 根目录（仅看非系统）")
    c_root = Path("C:\\")
    for d in c_root.iterdir():
        if d.is_dir() and not should_skip(d):
            s = count_files(d)
            if s.get('files', 0) > 0:
                print(f"  {d.name:40s}  files:{s.get('files', 0):6d}  md:{s.get('md', 0):4d}  size:{s.get('total_size', 0)/1024/1024:6.0f}MB")

    # 5. Eric 桌面 + 文档 (重点)
    print("\n[5] Eric 桌面 + 文档 (重点)")
    for p in [
        r"C:\Users\ericz\Desktop\张实项目总控",
        r"C:\Users\ericz\Desktop\obsidian",
        r"C:\Users\ericz\Documents\Obsidian",
        r"C:\Users\ericz\Documents\ObsidianVault",
        r"C:\Users\ericz\Music",
        r"D:\张实项目总控",
    ]:
        path = Path(p)
        if path.exists():
            s = count_files(path)
            print(f"  ✓ {p}  files:{s['files']}  md:{s['md']}  size:{s['total_size']/1024/1024:.0f}MB")


if __name__ == "__main__":
    main()
