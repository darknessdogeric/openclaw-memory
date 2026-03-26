# -*- coding: utf-8 -*-
import subprocess
import os
import json

def run_cmd(cmd_str):
    result = subprocess.run(['cmd', '/c', cmd_str], capture_output=True)
    return result.stdout

def decode_gbk(b):
    return b.decode('gbk', errors='replace')

def main():
    # First get the list of folders from F: drive
    raw = run_cmd('dir /ad /b F:\\')
    
    # Parse folders
    folders = []
    for f in raw.split(b'\r\n'):
        if f.strip():
            folders.append(decode_gbk(f.strip()))
    
    # Save to file
    with open('C:/Users/ericz/.openclaw/workspace/folder_list.json', 'w', encoding='utf-8') as out:
        json.dump({'folders': folders, 'raw_bytes': raw.hex()}, out, ensure_ascii=False, indent=2)
    
    print(f"Found {len(folders)} folders")
    print("Sample:", folders[:5] if folders else "None")

if __name__ == '__main__':
    main()
