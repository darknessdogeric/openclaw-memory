# -*- coding: utf-8 -*-
import subprocess
import json

def run_cmd(cmd_str):
    result = subprocess.run(['cmd', '/c', cmd_str], capture_output=True)
    return result.stdout

def decode_gbk(b):
    return b.decode('gbk', errors='replace')

# First get folder list from F: drive
raw_folders = run_cmd('dir F: /ad /b')
folders = [decode_gbk(f).strip() for f in raw_folders.split(b'\r\n') if f.strip()]

print("FOLDERS ON F: DRIVE:")
for i, f in enumerate(folders):
    print(f"  {i+1}. {f}")

# Build GBK encoded folder names
folder_gbk = {
    'manage': b'\xb9\xdc\xc0\xed\xcf\xee\xc4\xbf',      # 管理项目
    'ops': b'\xd4\xcb\xd3\xaa\xce\xc4\xbc\xfe',          # 运营文件
    'cts': b'\xd6\xd0\xc2\xc3\xbe\xc6\xb5\xea\xcf\xe0\xb9\xd8\xc4\xda\xc8\xdd',  # 中旅酒店相关内容
    'expand': b'\xd6\xd0\xbe\xc6\xcd\xd8\xd5\xb9',      # 中酒拓展
    'data': b'\xd6\xf7\xd2\xaa\xbe\xad\xd3\xaa\xca\xfd\xbe\xdd',  # 主要经营数据
    'reform': b'\xd7\xd4\xce\xd2\xb8\xef\xc3\xfc',       # 自我革命
    'xy': b'\xcf\xe5\xd1\xf4\xb9\xb2\xcf\xed\xb9\xfa\xbc\xca\xce\xc4\xbc\xfe',  # 襄阳共享国际文件
    'report': b'\xb8\xf6\xc8\xcb\xca\xc2\xcf\xee\xb1\xa8\xb8\xe6',  # 个人事项报告
    'media': b'\xd0\xc2\xc3\xbd\xcc\xe5',                # 新媒体
}

# Function to explore a folder by GBK name
def explore_by_gbk(gbk_name, description):
    name = gbk_name.decode('gbk')
    print(f"\n{'='*60}")
    print(f"EXPLORING: {description}")
    print(f"GBK: {gbk_name}")
    print(f"NAME: {name}")
    print('='*60)
    
    # Check if folder exists
    cmd = b'dir /ad /b "F:\\\\' + gbk_name + b'"'
    exist_raw = run_cmd(cmd.decode('gbk'))
    exist = decode_gbk(exist_raw).strip()
    
    if not exist:
        print("NOT FOUND")
        return None
    
    # Get files
    cmd = b'dir /a-d /o-s "F:\\\\' + gbk_name + b'"'
    files_raw = run_cmd(cmd.decode('gbk'))
    files_text = decode_gbk(files_raw)
    
    files = []
    for line in files_text.strip().split('\r\n'):
        parts = line.strip().split()
        if len(parts) >= 4:
            try:
                size_str = parts[2].replace(',', '')
                if size_str.isdigit() and int(size_str) > 0:
                    size = int(size_str)
                    fname = ' '.join(parts[3:])
                    if '.' in fname:
                        files.append({
                            'name': fname,
                            'size': size,
                            'size_mb': round(size / (1024*1024), 2)
                        })
            except:
                pass
    
    print(f"\nFILES ({len(files)}):")
    for f in files[:25]:
        print(f"  {f['name'][:55]:<55} {f['size_mb']:>8.2f} MB")
    
    # Get subfolders
    cmd = b'dir /ad /b "F:\\\\' + gbk_name + b'"'
    sub_raw = run_cmd(cmd.decode('gbk'))
    subfolders = [decode_gbk(s).strip() for s in sub_raw.split(b'\r\n') if s.strip()]
    
    if subfolders:
        print(f"\nSUBFOLDERS:")
        for sf in subfolders[:15]:
            print(f"  - {sf}")
    
    return {'name': name, 'files': files, 'subfolders': subfolders}

# Explore all priority folders
results = {}
for key, desc in [
    ('manage', 'Hotel Projects (管理项目)'),
    ('ops', 'Operations (运营文件)'),
    ('expand', 'Hotel Expansion (中酒拓展)'),
    ('cts', 'CTS Hotel Related (中旅酒店相关内容)'),
    ('data', 'Main Business Data (主要经营数据)'),
    ('reform', 'Self Revolution (自我革命)'),
    ('xy', 'Xiangyang Shared Docs (襄阳共享国际文件)'),
    ('report', 'Personal Reports (个人事项报告)'),
    ('media', 'New Media (新媒体)'),
]:
    result = explore_by_gbk(folder_gbk[key], desc)
    if result:
        results[key] = result

# Save to JSON
with open('C:/Users/ericz/.openclaw/workspace/priority_explored.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\n\nResults saved to priority_explored.json")
