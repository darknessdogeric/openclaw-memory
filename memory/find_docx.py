import os
import json
import sys

result = []
base = r'C:\Users\ericz\Desktop'

for root, dirs, files in os.walk(base):
    for fn in files:
        if fn.endswith('.docx') and '自我革命' in root:
            full = os.path.join(root, fn)
            rel = os.path.relpath(full, base)
            size_kb = os.path.getsize(full) / 1024
            result.append({
                'full': full,
                'rel': rel,
                'name': fn,
                'size_kb': round(size_kb, 1)
            })

with open(r'C:\Users\ericz\.openclaw\workspace\memory\docx_files.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Found {len(result)} files")
