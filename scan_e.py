# -*- coding: utf-8 -*-
import glob
import os
import sys

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

dirs = [
    'E:/2024预算/',
    'E:/主要经营数据/',
    'E:/损益经营类/',
    'E:/经营文件/',
    'E:/项目测算/',
    'E:/自我革命/',
]

all_files = []

for d in dirs:
    if os.path.exists(d):
        files = glob.glob(d + '*')
        print(f'\n=== {d} ({len(files)} files) ===')
        for f in files[:40]:
            name = os.path.basename(f)
            ext = os.path.splitext(name)[1].lower()
            all_files.append({'path': f, 'name': name, 'ext': ext, 'dir': d})
            print(f'  [{ext}] {name}')
        if len(files) > 40:
            print(f'  ... and {len(files)-40} more')
    else:
        print(f'\n=== {d} - NOT FOUND ===')

print(f'\n\nTotal files found: {len(all_files)}')
print('\nFile types:')
from collections import Counter
ext_count = Counter(f['ext'] for f in all_files)
for ext, count in ext_count.most_common():
    print(f'  {ext}: {count}')
