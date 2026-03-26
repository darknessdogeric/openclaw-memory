with open('C:/Users/ericz/.openclaw/workspace/memory/hotel-industry-knowledge-base.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Read current TOC lines
lines = content.split('\n')
in_toc = False
toc_lines = []
for i, line in enumerate(lines):
    if '## 目录' in line:
        in_toc = True
    if in_toc:
        toc_lines.append((i, line))
        if '4.8' in line and '第四空间' in line:
            break

# Find where 4.7.4 starts in TOC
start_idx = None
for i, line in lines:
    if '4.7.4' in line:
        start_idx = i
        break

# Print the relevant TOC lines
for idx, line in toc_lines:
    if '4.7' in line:
        print(f'{idx}: {line[:100]}')
