# -*- coding: utf-8 -*-
import subprocess
import os
import json

def run_cmd(cmd):
    result = subprocess.run(['cmd', '/c', cmd], capture_output=True)
    return result.stdout

def explore_all():
    results = {}
    
    # Test if we can access F: drive
    test = run_cmd('dir F: /ad /b')
    test_str = test.decode('gbk', errors='replace')
    
    # Save raw test
    with open('C:/Users/ericz/.openclaw/workspace/test_raw.bin', 'wb') as f:
        f.write(test)
    
    # Try folder by folder
    folders_to_test = [
        'F:\\管理项目',
        'F:\\运营文件', 
        'F:\\自我革命',
        'F:\\主要经营数据',
        'F:\\新媒体',
    ]
    
    for folder in folders_to_test:
        # Check if folder exists
        exist_cmd = f'dir /ad /b "{folder}"'
        exist_result = run_cmd(exist_cmd)
        exist_str = exist_result.decode('gbk', errors='replace').strip()
        
        if exist_str and not exist_str.startswith('File Not Found'):
            print(f"EXISTS: {folder}")
            
            # Get files
            files_cmd = f'dir /a-d /o-s "{folder}"'
            files_result = run_cmd(files_cmd)
            files_str = files_result.decode('gbk', errors='replace')
            
            results[folder] = {
                'exists': True,
                'files_output': files_str
            }
        else:
            print(f"NOT FOUND: {folder}")
            results[folder] = {'exists': False}
    
    # Save results
    with open('C:/Users/ericz/.openclaw/workspace/explore_results.json', 'w', encoding='utf-8') as f:
        # Convert bytes to strings for JSON
        json.dump({k: {kk: vv for kk, vv in v.items()} for k, v in results.items()}, f, ensure_ascii=False, indent=2)
    
    print("\nResults saved to explore_results.json")

if __name__ == '__main__':
    explore_all()
