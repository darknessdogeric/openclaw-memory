# -*- coding: utf-8 -*-
import subprocess
import json
import os

def run_cmd(cmd_str):
    result = subprocess.run(['cmd', '/c', cmd_str], capture_output=True)
    return result.stdout.decode('gbk', errors='replace')

def get_folder_files(folder_name):
    """Get files in a folder with sizes"""
    cmd = f'dir /a-d /o-s "F:\\{folder_name}"'
    raw = run_cmd(cmd)
    
    files = []
    for line in raw.strip().split('\r\n'):
        parts = line.strip().split()
        if len(parts) >= 4:
            try:
                # Size is usually the 3rd column (index 2)
                size_str = parts[2].replace(',', '')
                if size_str.isdigit() and int(size_str) > 0:
                    size = int(size_str)
                    # Filename is everything after the date/time columns
                    # Format: MM/DD/YYYY HH:MM  AM/PM  SIZE  FILENAME
                    # or: MM/DD/YYYY HH:MM  SIZE  FILENAME
                    name = ' '.join(parts[3:])
                    if '.' in name and not name.startswith('.'):
                        files.append({
                            'name': name,
                            'size': size,
                            'size_mb': round(size / (1024*1024), 2)
                        })
            except:
                pass
    return files

def get_subfolders(folder_name):
    """Get subfolders in a folder"""
    cmd = f'dir /ad /b "F:\\{folder_name}"'
    raw = run_cmd(cmd)
    return [f.strip() for f in raw.strip().split('\r\n') if f.strip()]

def explore_folder(folder_name, folder_desc):
    """Explore a folder comprehensively"""
    print(f"\n{'='*70}")
    print(f"FOLDER: {folder_name}")
    print(f"DESCRIPTION: {folder_desc}")
    print('='*70)
    
    # Check if folder exists
    exist_cmd = f'dir /ad /b "F:\\{folder_name}"'
    exist_raw = run_cmd(exist_cmd)
    if not exist_raw.strip():
        print("FOLDER NOT FOUND")
        return None
    
    # Get files
    files = get_folder_files(folder_name)
    print(f"\nFILES ({len(files)} total, showing top 30 by size):")
    for f in files[:30]:
        print(f"  {f['name'][:60]:<60} {f['size_mb']:>8.2f} MB")
    
    # Get subfolders
    subfolders = get_subfolders(folder_name)
    if subfolders:
        print(f"\nSUBFOLDERS ({len(subfolders)}):")
        for sf in subfolders[:20]:
            print(f"  - {sf}")
    
    return {
        'name': folder_name,
        'desc': folder_desc,
        'files': files,
        'subfolders': subfolders
    }

# Priority folders to explore
priority_folders = [
    ('管理项目', 'Hotel Projects - 酒店项目'),
    ('运营文件', 'Operations Files - 运营文件'),
    ('中旅酒店相关内容', 'CTS Hotel Related - 中旅酒店相关内容'),
    ('中酒拓展', 'Hotel Expansion - 中酒拓展'),
    ('主要经营数据', 'Main Business Data - 主要经营数据'),
    ('自我革命', 'Self Revolution - 自我革命'),
    ('襄阳共享国际文件', 'Xiangyang Shared Intl Docs'),
    ('个人事项报告', 'Personal Reports'),
    ('新媒体', 'New Media'),
]

results = {}
for folder, desc in priority_folders:
    result = explore_folder(folder, desc)
    if result:
        results[folder] = result

# Save results
with open('C:/Users/ericz/.openclaw/workspace/explored_folders.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\n\n=== SUMMARY ===")
for folder, data in results.items():
    print(f"{folder}: {len(data['files'])} files, {len(data['subfolders'])} subfolders")
