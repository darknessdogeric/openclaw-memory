with open('C:/Users/ericz/.openclaw/workspace/memory/hotel-industry-knowledge-base.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()
print(f'Total lines: {len(lines)}')
print(f'Total chars: {sum(len(l) for l in lines)}')
for i, l in enumerate(lines):
    stripped = l.strip()
    if stripped.startswith('## '):
        print(f'Line {i}: {stripped[:100]}')
