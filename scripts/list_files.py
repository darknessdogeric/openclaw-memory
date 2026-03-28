# -*- coding: utf-8 -*-
import os, subprocess, sys

folder = r'E:\桌面20250702'

# Get file list with proper Unicode
result = subprocess.run(
    ['cmd', '/c', 'chcp 65001 >nul 2>&1 && dir /b "' + folder + '"'],
    capture_output=True
)
content = result.stdout.decode('gbk', errors='replace')
files = [f.strip() for f in content.split('\r\n') if f.strip()]

# Print to stdout for capture
for i, f in enumerate(files):
    print(f'{i:2d}. {f}')

# Save to a temp file for reference
with open(r'C:\Users\ericz\.openclaw\workspace\scripts\file_list.txt', 'w', encoding='utf-8') as out:
    for f in files:
        out.write(f + '\n')
