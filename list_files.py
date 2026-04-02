# -*- coding: utf-8 -*-
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# List files in budget directories
dirs = [r'E:\2024预算', r'E:\2023年预算工作', r'E:\桌面']
for d in dirs:
    if os.path.exists(d):
        print(f'\n=== {d} ===')
        for f in os.listdir(d):
            full = os.path.join(d, f)
            print(f'  {repr(f)} -> {f}')
    else:
        print(f'\n=== {d} - NOT FOUND ===')
