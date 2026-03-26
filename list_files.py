# -*- coding: utf-8 -*-
import os

desktop = r'C:\Users\ericz\Desktop'

# Find the hotel migration folder
hotel_folder = None
ahl_folder = None

for entry in os.scandir(desktop):
    name = entry.name
    if 'AHL' in name and entry.is_dir():
        ahl_folder = entry.path
    elif 'hotel' in name.lower() or 'migration' in name.lower() or '\u9152\u5e97' in name or '\u77e5\u8bc6' in name:
        if entry.is_dir():
            hotel_folder = entry.path

results = []

results.append('=== Hotel Migration Folder ===')
results.append(f'Path: {hotel_folder}')

if hotel_folder:
    for root, dirs, files in os.walk(hotel_folder):
        for f in files:
            fp = os.path.join(root, f)
            size = os.path.getsize(fp)
            rel = fp.replace(hotel_folder, '').lstrip('\\')
            results.append(f'  {rel} ({size//1024}KB)')

results.append('')
results.append('=== AHL-Database Folder ===')
results.append(f'Path: {ahl_folder}')

if ahl_folder:
    for root, dirs, files in os.walk(ahl_folder):
        level = root.replace(ahl_folder, '').count(os.sep)
        indent = '  ' * level
        results.append(f'{indent}{os.path.basename(root)}/')
        subindent = '  ' * (level + 1)
        for f in files:
            fp = os.path.join(root, f)
            size = os.path.getsize(fp)
            results.append(f'{subindent}{f} ({size//1024}KB)')

output_path = r'C:\Users\ericz\Desktop\all_source_files.txt'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(results))

print(f'Done. Wrote to {output_path}')
