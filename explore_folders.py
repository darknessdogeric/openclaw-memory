import subprocess
import os
import sys

def get_cmd_output(cmd):
    """Run cmd command and return output as proper string"""
    result = subprocess.run(['cmd', '/c', cmd], capture_output=True)
    raw_bytes = result.stdout
    return raw_bytes.decode('gbk', errors='replace')

def list_folder_contents(folder_path):
    """List all files in a folder with sizes"""
    cmd = f'dir "{folder_path}" /b /a-d'
    output = get_cmd_output(cmd)
    files = []
    for line in output.strip().split('\r\n'):
        if line.strip():
            files.append(line.strip())
    return files

def get_folder_size(folder_path):
    """Get total size of folder"""
    cmd = f'dir "{folder_path}" /s /a-d'
    output = get_cmd_output(cmd)
    # Parse total bytes from output like "Total Files: 123 bytes"
    lines = output.strip().split('\r\n')
    for line in lines[-5:]:
        if 'bytes' in line.lower() and 'dir(s)' not in line.lower():
            try:
                # Extract number
                parts = line.split()
                for p in parts:
                    if p.replace(',', '').replace('.', '').isdigit():
                        return int(p.replace(',', ''))
            except:
                pass
    return 0

def explore_priority_folders():
    """Explore priority folders on F: drive"""
    
    # Folder mapping from garbled to clear names
    folder_map = {
        '管理项目': 'F:/管理项目',
        '运营文件': 'F:/运营文件', 
        '中酒拓展': 'F:/中酒拓展',
        '中旅酒店相关内容': 'F:/中旅酒店相关内容',
        '主要经营数据': 'F:/主要经营数据',
        '自我革命': 'F:/自我革命',
        '襄阳共享国际文件': 'F:/襄阳共享国际文件',
        '个人事项报告': 'F:/个人事项报告',
        '2023年预算工作': 'F:/2023年预算工作',
        '2024预算': 'F:/2024预算',
        '新媒体': 'F:/新媒体',
        '保留意见': 'F:/保留意见',
        '述职报告': 'F:/述职报告',
        '餐饮协会应收证据': 'F:/餐饮协会应收证据',
        '车险': 'F:/车险',
    }
    
    results = {}
    
    for folder_name, folder_path in folder_map.items():
        if not os.path.exists(folder_path):
            print(f"NOT FOUND: {folder_name} at {folder_path}")
            continue
            
        print(f"\n{'='*60}")
        print(f"EXPLORING: {folder_name}")
        print(f"PATH: {folder_path}")
        print('='*60)
        
        # Get all files
        cmd = f'dir "{folder_path}" /b /a-d /o-s'  # /o-s = sort by size descending
        output = get_cmd_output(cmd)
        files = [f.strip() for f in output.strip().split('\r\n') if f.strip() and '.' in f]
        
        print(f"\nFiles ({len(files)}):")
        
        file_info = []
        for f in files[:30]:  # First 30 files
            full_path = os.path.join(folder_path, f)
            try:
                size = os.path.getsize(full_path)
                size_mb = size / (1024*1024)
                file_info.append((f, size, size_mb))
                print(f"  {f[:50]:<50} {size_mb:.2f} MB")
            except Exception as e:
                print(f"  {f[:50]:<50} ERROR: {e}")
        
        results[folder_name] = {
            'path': folder_path,
            'files': file_info,
            'total_count': len(files)
        }
        
        # Check for subdirectories
        subdirs_cmd = f'dir "{folder_path}" /b /ad'
        subdirs_output = get_cmd_output(subdirs_cmd)
        subdirs = [s.strip() for s in subdirs_output.strip().split('\r\n') if s.strip()]
        if subdirs:
            print(f"\nSubfolders: {', '.join(subdirs[:10])}")
    
    return results

if __name__ == '__main__':
    results = explore_priority_folders()
    print("\n\nSUMMARY:")
    for name, info in results.items():
        print(f"{name}: {info['total_count']} files")
