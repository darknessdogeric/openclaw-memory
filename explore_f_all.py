import os

drive = 'F:/'

def list_all(path, indent=0):
    prefix = '  ' * indent
    try:
        items = sorted(os.listdir(path))
        dirs = []
        files = []
        for item in items:
            if item.startswith('$') or item == 'System Volume Information':
                continue
            full = os.path.join(path, item)
            if os.path.isdir(full):
                dirs.append((item, full))
            else:
                try:
                    sz = os.path.getsize(full)
                    files.append((item, sz))
                except:
                    pass
        # Print dirs first
        for name, full in dirs:
            print(f'{prefix}[DIR]  {name}/')
            list_all(full, indent+1)
        # Then files
        for name, sz in files:
            kb = sz // 1024
            if kb > 1024:
                size_str = f'{kb//1024}MB'
            else:
                size_str = f'{kb}KB'
            print(f'{prefix}[FILE] {name} ({size_str})')
    except Exception as e:
        print(f'{prefix}ERROR: {e}')

print(f'F:/ FULL DIRECTORY TREE')
print('='*60)
list_all(drive)
print()
print('='*60)
# Also get total count
total_files = 0
total_dirs = 0
for root, dirs, files in os.walk(drive):
    if '$RECYCLE.BIN' in root or 'System Volume' in root:
        continue
    total_dirs += len(dirs)
    total_files += len(files)
print(f'Total: {total_dirs} dirs, {total_files} files')
