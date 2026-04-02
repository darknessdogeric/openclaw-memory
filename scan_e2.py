# -*- coding: utf-8 -*-
import glob
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

dirs_to_scan = [
    'E:/2024预算/',
    'E:/2023年预算工作/',
    'E:/主要经营数据/',
    'E:/中旅酒店相关内容/',
    'E:/自我革命/',
    'E:/管理项目/',
    'E:/运营文件/',
    'E:/述职报告/',
    'E:/桌面/',
    'E:/桌面20250702/',
    'E:/保留意见/',
    'E:/分管部门/',
    'E:/襄阳共享国际文件/',
]

all_files = []

for d in dirs_to_scan:
    if os.path.exists(d):
        files = glob.glob(d + '*')
        print(f'\n=== {d} ({len(files)} files) ===')
        for f in files[:50]:
            name = os.path.basename(f)
            ext = os.path.splitext(name)[1].lower()
            if not ext:
                ext = '[DIR]'
            all_files.append({'path': f, 'name': name, 'ext': ext, 'dir': d})
            print(f'  [{ext}] {name}')
        if len(files) > 50:
            print(f'  ... and {len(files)-50} more')
    else:
        print(f'\n=== {d} - NOT FOUND ===')

print(f'\n\nTotal items found: {len(all_files)}')
from collections import Counter
ext_count = Counter(f['ext'] for f in all_files)
print('\nFile types:')
for ext, count in sorted(ext_count.items(), key=lambda x: -x[1]):
    print(f'  {ext}: {count}')

# Show all xlsx, pdf, docx, doc files
print('\n=== KEY FINANCIAL FILES (xlsx/pdf/docx/doc) ===')
key_exts = ['.xlsx', '.pdf', '.docx', '.doc', '.xls', '.pptx']
for f in all_files:
    if f['ext'] in key_exts:
        print(f"  {f['dir']} | {f['name']}")
