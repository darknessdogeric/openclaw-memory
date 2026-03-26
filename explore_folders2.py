import subprocess
import os
import sys

# Force UTF-8 mode for Python
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def get_cmd_output(cmd):
    """Run cmd command and return output as proper string"""
    result = subprocess.run(['cmd', '/c', cmd], capture_output=True)
    raw_bytes = result.stdout
    return raw_bytes.decode('gbk', errors='replace')

def list_dir_formatted(folder_bytes_path):
    """List directory contents with sizes"""
    # Use cmd dir with size
    cmd = f'dir /a-d /o-s "{folder_bytes_path.decode(\'gbk\')}"'
    output = get_cmd_output(cmd)
    return output

def explore_folders():
    """Explore priority folders on F: drive using raw bytes"""
    
    # Priority folders (bytes paths)
    folders = [
        (b'F:\\管理项目', '管理项目 (Hotel Projects)'),
        (b'F:\\运营文件', '运营文件 (Operations)'),
        (b'F:\\中酒拓展', '中酒拓展 (Hotel Expansion)'),
        (b'F:\\中旅酒店相关内容', '中旅酒店相关内容'),
        (b'F:\\主要经营数据', '主要经营数据 (Main Business Data)'),
        (b'F:\\自我革命', '自我革命 (Self Revolution)'),
        (b'F:\\襄阳共享国际文件', '襄阳共享国际文件'),
        (b'F:\\个人事项报告', '个人事项报告'),
        (b'F:\\新媒体', '新媒体 (New Media)'),
        (b'F:\\述职报告', '述职报告 (Work Reports)'),
    ]
    
    results = {}
    
    for path_bytes, name in folders:
        path_str = path_bytes.decode('gbk')
        if not os.path.exists(path_str):
            print(f"\n{'='*60}")
            print(f"NOT FOUND: {name}")
            print(f"Path: {path_str}")
            print('='*60)
            continue
            
        print(f"\n{'='*60}")
        print(f"EXPLORING: {name}")
        print(f"PATH: {path_str}")
        print('='*60)
        
        # Get directory listing
        cmd = f'dir /a-d /o-s "{path_str}"'
        output = get_cmd_output(cmd)
        
        lines = output.strip().split('\r\n')
        
        # Parse files
        files = []
        for line in lines:
            # Look for lines with file info (has date and time)
            parts = line.strip().split()
            if len(parts) >= 4:
                # Try to find size (usually second-to-last or third item)
                try:
                    # Check if last parts look like size
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
        sub_cmd = f'dir /ad /b "{path_str}"'
        sub_output = get_cmd_output(sub_cmd)
        subdirs = [s.strip() for s in sub_output.strip().split('\r\n') if s.strip()]
        if subdirs:
            print(f"\nSubdirectories: {', '.join(subdirs[:15])}")
        
        results[name] = {
            'path': path_str,
            'files': files,
            'subdirs': subdirs
        }
    
    return results

if __name__ == '__main__':
    try:
        results = explore_folders()
    except Exception as e:
        import traceback
        traceback.print_exc()
