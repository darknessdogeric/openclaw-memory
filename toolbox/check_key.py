import re
with open(r'D:\B166ER-OpenClaw\openclaw.json', 'r', encoding='utf-8') as f:
    content = f.read()
matches = re.findall(r'"(sk-[A-Za-z0-9_-]+)"', content)
print(f'Found {len(matches)} sk- keys in openclaw.json')
for i, m in enumerate(matches):
    visible = m[:4] + '...' + m[-4:] if len(m) > 12 else m
    print(f'  [{i+1}] {visible} (len={len(m)})')