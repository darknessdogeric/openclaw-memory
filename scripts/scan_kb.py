import os, glob, time

d = r'C:\Users\Administrator\.openclaw\workspace\memory'
files = sorted(glob.glob(os.path.join(d, '*.md')))
total_kb = 0
for f in files:
    name = os.path.basename(f)
    size = os.path.getsize(f)
    total_kb += size
    mtime = time.strftime('%Y-%m-%d', time.localtime(os.path.getmtime(f)))
    print(f'{name:55s} {size/1024:7.1f}KB  {mtime}')

print(f'\nTotal: {len(files)} KB files, {total_kb/1024:.1f} KB')
