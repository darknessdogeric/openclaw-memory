with open('C:/Users/ericz/.openclaw/workspace/memory/hotel-industry-knowledge-base.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find TOC section
in_toc = False
for i, line in enumerate(lines):
    if '## 目录' in line:
        in_toc = True
    if in_toc and '4.8' in line and '第四空间' in line:
        break
    if in_toc and '4.7' in line:
        print(f'{i}: {line.rstrip()[:100]}')
