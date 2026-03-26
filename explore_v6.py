# -*- coding: utf-8 -*-
import subprocess
import os

def gbk(s):
    return s.encode('gbk')

def decode_gbk(b):
    return b.decode('gbk', errors='replace')

def run_cmd(cmd_str):
    result = subprocess.run(['cmd', '/c', cmd_str], capture_output=True)
    return result.stdout

def main():
    # First get the list of folders from F: drive
    raw = run_cmd('dir /ad /b F:\\')
    folders = [decode_gbk(f) for f in raw.split(b'\r\n') if f.strip()]
    
    print("=== ALL FOLDERS ON F: ===")
    for i, f in enumerate(folders):
        print(f"  {i+1}. {f}")
    
    print("\n=== CHECKING PRIORITY FOLDERS ===")
    
    # These are the names we need to find
    priority_names = [
        '管理项目', '运营文件', '中酒拓展', '中旅酒店相关内容',
        '主要经营数据', '自我革命', '襄阳共享国际文件',
        '个人事项报告', '新媒体', '述职报告'
    ]
    
    found = {}
    for pname in priority_names:
        for fname in folders:
            if pname in fname or fname in pname:
                found[pname] = fname
                break
    
    print("\nPriority folder mapping:")
    for pname in priority_names:
        if pname in found:
            print(f"  {pname} -> {found[pname]} [FOUND]")
        else:
            print(f"  {pname} -> [NOT FOUND]")
    
    # Now explore each found folder
    print("\n=== EXPLORING FOUND FOLDERS ===")
    for pname, fname in found.items():
        print(f"\n--- {fname} ---")
        cmd = f'dir /a-d /o-s "F:\\{fname}"'
        raw = run_cmd(cmd)
        text = decode_gbk(raw)
        
        # Parse and show files
        lines = text.strip().split('\r\n')
        file_count = 0
        for line in lines:
            # Look for file lines (has size and name)
            parts = line.strip().split()
            if len(parts) >= 4:
                try:
                    size_str = parts[2].replace(',', '')
                    if size_str.isdigit() and int(size_str) > 0:
                        size = int(size_str)
                        name = ' '.join(parts[3:])
                        if '.' in name and not name.startswith('.'):
                            file_count += 1
                            if file_count <= 20:
                                size_mb = size / (1024*1024)
                                print(f"    {name[:55]:<55} {size_mb:>8.2f} MB")
                except:
                    pass
        
        print(f"  Total files shown: {file_count}")

if __name__ == '__main__':
    main()
