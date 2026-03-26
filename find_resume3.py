import os, sys
sys.stdout.reconfigure(encoding='utf-8')

desktop = 'C:/Users/ericz/Desktop'
items = os.listdir(desktop)
results = []
for f in items:
    if not os.path.isdir(os.path.join(desktop, f)):
        sz = os.path.getsize(os.path.join(desktop, f))
        results.append(f'{sz//1024:>6}KB  {f}')

with open('C:/Users/ericz/.openclaw/workspace/desktop_files.txt', 'w', encoding='utf-8') as out:
    for r in sorted(results):
        out.write(r + '\n')
print('Done, written', len(results), 'files')
