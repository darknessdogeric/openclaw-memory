import os
f = 'memory/hotel-industry-knowledge-base.md'
sz = os.path.getsize(f)
with open(f, 'r', encoding='utf-8') as fh:
    content = fh.read()
    lines = content.split('\n')
    chars = len(content)

print(f'File: {sz/1024:.0f} KB | Lines: {len(lines):,} | Chars: {chars:,}')
print(f'Created: 2026-02-13 | Updated: 2026-03-28')
print()

# Count sections
sec2 = sec3 = sec4 = 0
for l in lines:
    s = l.strip()
    if s.startswith('## ') and not s.startswith('###'):
        sec2 += 1
    elif s.startswith('### '):
        sec3 += 1
    elif s.startswith('#### '):
        sec4 += 1
print(f'Structure: {sec2} chapters | {sec3} sections | {sec4} subsections')
print()

# Show key sections (just the ## ones)
for l in lines:
    s = l.strip()
    if s.startswith('## ') and not s.startswith('###'):
        print(f'  {s}')
