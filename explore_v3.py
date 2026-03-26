# -*- coding: utf-8 -*-
import subprocess
import os
import sys

def get_cmd_output(cmd):
    result = subprocess.run(['cmd', '/c', cmd], capture_output=True)
    return result.stdout.decode('gbk', errors='replace')

def explore_folders():
    folders = [
        'F:\\管理项目',
        'F:\\运营文件',
        'F:\\中酒拓展',
        'F:\\中旅酒店相关内容',
        'F:\\主要经营数据',
        'F:\\自我革命',
        'F:\\襄阳共享国际文件',
        'F:\\个人事项报告',
        'F:\\新媒体',
        'F:\\述职报告',
    ]
    
    folder_names = {
        'F:\\管理项目': '管理项目 (Hotel Projects)',
        'F:\\运营文件': '运营文件 (Operations)',
        'F:\\中酒拓展': '中酒拓展 (Hotel Expansion)',
        'F:\\中旅酒店相关内容': '中旅酒店相关内容',
        'F:\\主要经营数据': '主要经营数据 (Main Business Data)',
        'F:\\自我革命': '自我革命 (Self Revolution)',
        'F:\\襄阳共享国际文件': '襄阳共享国际文件',
        'F:\\个人事项报告': '个人事项报告',
        'F:\\新媒体': '新媒体 (New Media)',
        'F:\\述职报告': '述职报告 (Work Reports)',
    }
    
    results = {}
    
    for folder in folders:
        name = folder_names.get(folder, folder)
        
        if not os.path.exists(folder):
            print(f"\n{'='*60}")
            print(f"NOT FOUND: {name}")
            print(f"Path: {folder}")
            print('='*60)
            continue
            
        print(f"\n{'='*60}")
        print(f"EXPLORING: {name}")
        print(f"PATH: {folder}")
        print('='*60)
        
        # Get directory listing with sizes
        cmd = 'dir /a-d /o-s "' + folder + '"'
        output = get_cmd_output(cmd)
        
        lines = output.strip().split('\r\n')
        
        # Parse files
        files = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) >= 4:
                try:
                    for i, p in enumerate(parts):
                        p_clean = p.replace(',', '').replace('.', '')
                        if p_clean.isdigit() and int(p_clean) > 0:
                            size = int(p_clean)
                            filename = ' '.join(parts[i+1:])
                            if '.' in filename:
                                files.append((filename, size))
                                break
                except:
                    pass
        
        print(f"\nFiles found: {len(files)}")
        for fname, size in files[:30]:
            size_mb = size / (1024*1024)
            print(f"  {fname[:60]:<60} {size_mb:>8.2f} MB")
        
        # Get subdirectories
        sub_cmd = 'dir /ad /b "' + folder + '"'
        sub_output = get_cmd_output(sub_cmd)
        subdirs = [s.strip() for s in sub_output.strip().split('\r\n') if s.strip()]
        if subdirs:
            print(f"\nSubdirectories: {', '.join(subdirs[:15])}")
        
        results[name] = {
            'path': folder,
            'files': files[:50],
            'subdirs': subdirs
        }
    
    return results

if __name__ == '__main__':
    try:
        results = explore_folders()
    except Exception as e:
        import traceback
        traceback.print_exc()
