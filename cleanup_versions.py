#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理KB版本文件 - 保留最新版，归档旧版"""
import os, shutil
from pathlib import Path

mem = Path('C:/Users/ericz/.openclaw/workspace/memory')
archive = mem / 'archive_versions'
archive.mkdir(exist_ok=True)

def parse_ver(name):
    """Extract version number from filename"""
    import re
    m = re.search(r'-v(\d+(?:\.\d+)?)', name)
    if m:
        v = m.group(1)
        return float(v) if '.' in v else int(v)
    return None

# Group files by KB base name
kb_groups = {}
for f in mem.glob('*.md'):
    if f.stem.startswith('2026-'):
        continue
    name = f.stem
    base = name
    ver = parse_ver(name)
    for suffix in ['-v7','-v6','-v5','-v4','-v3.0','-v3','-v2','-v1']:
        if name.endswith(suffix):
            base = name[:-len(suffix)]
            break
    if base not in kb_groups:
        kb_groups[base] = []
    kb_groups[base].append((ver, name, f))

to_archive = []

for base, files in kb_groups.items():
    # Separate versioned vs main (no version) files
    versioned = [(v, n, f) for v, n, f in files if v is not None]
    main_files = [(n, f) for v, n, f in files if v is None]
    
    if versioned:
        # Find latest version
        latest_ver, latest_name, latest_file = max(versioned, key=lambda x: x[0])
        print(f'KB: {base}')
        print(f'  Latest: {latest_name} ({latest_file.stat().st_size//1024}KB)')
        
        # Mark older versions for archiving
        for v, n, f in versioned:
            if f != latest_file:
                to_archive.append((f, f'{base}_v{v}_{f.name}'))
                print(f'  Archive: {n} ({f.stat().st_size//1024}KB)')
        
        # If there's also a main file (no version), archive it too
        for n, f in main_files:
            # Main file is likely older than latest version
            to_archive.append((f, f'{base}_main_{f.name}'))
            print(f'  Archive main: {n} ({f.stat().st_size//1024}KB)')
    elif main_files:
        # No version info, skip (these are unique KBs)
        for n, f in main_files:
            print(f'  Keep (no version): {n}')

print(f'\nTotal to archive: {len(to_archive)} files')
print(f'Will save approximately: {sum(f.stat().st_size for f, _ in to_archive)//1024}KB')

# Confirm and execute
confirm = input('\nProceed with archiving? (y/n): ')
if confirm.lower() == 'y':
    for src, dst_name in to_archive:
        dst = archive / dst_name
        shutil.copy2(src, dst)
    print(f'Archived {len(to_archive)} files to {archive}')
else:
    print('Cancelled')
