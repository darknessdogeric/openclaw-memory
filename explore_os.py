# -*- coding: utf-8 -*-
import os
import json

def explore_folder(folder_bytes):
    """Explore a folder and return its contents"""
    # Use bytes path
    folder_path = b'F:/' + b'/' + folder_bytes
    
    if not os.path.isdir(folder_path):
        return None
    
    files = []
    subfolders = []
    
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        
        if os.path.isdir(item_path):
            subfolders.append(item.decode('utf-8', errors='replace'))
        elif os.path.isfile(item_path):
            size = os.path.getsize(item_path)
            files.append({
                'name': item.decode('utf-8', errors='replace'),
                'size': size,
                'size_mb': round(size / (1024*1024), 2)
            })
    
    # Sort by size descending
    files.sort(key=lambda x: x['size'], reverse=True)
    subfolders.sort()
    
    return {
        'folder': folder_bytes.decode('utf-8'),
        'path': folder_path.decode('utf-8'),
        'files': files,
        'subfolders': subfolders
    }

# Priority folders (UTF-8 encoded bytes from os.listdir output)
priority_folders = [
    b'\xe7\xae\xa1\xe7\x90\x86\xe9\xa1\xb9\xe7\x9b\xae',  # 管理项目
    b'\xe8\xbf\x90\xe8\x90\xa5\xe6\x96\x87\xe4\xbb\xb6',  # 运营文件
    b'\xe4\xb8\xad\xe6\x97\x85\xe9\x85\x92\xe5\xba\x97\xe7\x9b\xb8\xe5\x85\xb3\xe5\x86\x85\xe5\xae\xb9',  # 中旅酒店相关内容
    b'\xe4\xb8\xad\xe9\x85\x92\xe6\x8b\x93\xe5\xb1\x95',  # 中酒拓展
    b'\xe4\xb8\xbb\xe8\xa6\x81\xe7\xbb\x8f\xe8\x90\xa5\xe6\x95\xb0\xe6\x8d\xae',  # 主要经营数据
    b'\xe8\x87\xaa\xe6\x88\x91\xe9\x9d\xa9\xe5\x91\xbd',  # 自我革命
    b'\xe8\xa5\x84\xe9\x98\xb3\xe5\x85\xb1\xe4\xba\xab\xe5\x9b\xbd\xe9\x99\x85\xe6\x96\x87\xe4\xbb\xb6',  # 襄阳共享国际文件
    b'\xe4\xb8\xaa\xe4\xba\xba\xe4\xba\x8b\xe9\xa1\xb9\xe6\x8a\xa5\xe5\x91\x8a',  # 个人事项报告
    b'\xe6\x96\xb0\xe5\xaa\x92\xe4\xbd\x93',  # 新媒体
]

results = {}

for folder_bytes in priority_folders:
    folder_name = folder_bytes.decode('utf-8')
    result = explore_folder(folder_bytes)
    
    if result:
        results[folder_name] = result
        print(f"\n{'='*60}")
        print(f"FOLDER: {folder_name}")
        print(f"PATH: {result['path']}")
        print(f"FILES: {len(result['files'])}")
        print(f"SUBFOLDERS: {len(result['subfolders'])}")
        print('='*60)
        
        if result['files']:
            print("\nTop files by size:")
            for f in result['files'][:20]:
                print(f"  {f['name'][:55]:<55} {f['size_mb']:>8.2f} MB")
        
        if result['subfolders']:
            print(f"\nSubfolders: {', '.join(result['subfolders'][:15])}")
    else:
        print(f"\nNOT FOUND: {folder_name}")

# Save to JSON
with open('C:/Users/ericz/.openclaw/workspace/priority_explored.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\n\nResults saved to priority_explored.json")
