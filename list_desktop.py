# -*- coding: utf-8 -*-
import os

desktop = r'C:\Users\ericz\Desktop'

results = []

for entry in os.scandir(desktop):
    name = entry.name
    is_dir = entry.is_dir()
    tag = '[DIR]' if is_dir else '[FILE]'
    size = entry.stat().st_size if not is_dir else 0
    results.append(f'{tag}|{name}|{size}')

with open(r'C:\Users\ericz\Desktop\desktop_list.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(results))

print('Done, wrote', len(results), 'entries')
