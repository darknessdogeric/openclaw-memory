from pathlib import Path
import re

files = sorted(Path('reports').glob('2026-07-16-新能源车外挂小蓝灯-*.md'))
files = [f for f in files if '全网扒数据' not in f.name]

for f in files:
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    content = f.read_text(encoding='utf-8')
    lines = content.split('\n')
    print('=' * 60)
    print(f'FILE: {f.name}  ({len(content)} chars / {len(content.encode("utf-8"))//1024}KB)')
    print('--- HEAD ---')
    for i, l in enumerate(lines[:30]):
        clean = re.sub(r'^\s+', '', l)
        if clean and not clean.startswith('---'):
            print(f'{i:3} | {clean[:120].encode("ascii", "ignore").decode("ascii", "ignore") if False else clean[:120]}')
    print()
