# -*- coding: utf-8 -*-
import subprocess
import json

result = subprocess.run(['cmd', '/c', 'dir F: /ad /b'], capture_output=True)
raw = result.stdout

# Decode as GBK
text = raw.decode('gbk', errors='replace')

# Save to JSON
folders = [f.strip() for f in text.split('\r\n') if f.strip()]

data = {
    'raw_bytes_hex': raw.hex(),
    'folders': folders,
    'count': len(folders)
}

with open('C:/Users/ericz/.openclaw/workspace/folder_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Found {len(folders)} folders")
for folder in folders:
    print(f"  - {folder}")
