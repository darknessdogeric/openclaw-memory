import sys, json, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'D:\B166ER-OpenClaw\workspace\outputs\酒管公司供应链工程-交付包-v1.0\04-思维导图\酒管公司供应链工程-思维导图.html', 'r', encoding='utf-8') as f:
    html = f.read()

m = re.search(r'const data = (\{.*?\});\s*\n', html, re.DOTALL)
if not m:
    print('NO MATCH')
    sys.exit(1)
data = json.loads(m.group(1))

print(f'Root: {data["content"]}')
print(f'Root children count: {len(data["children"])}')

def count(n):
    c = 1
    for ch in n.get('children', []):
        c += count(ch)
    return c

def depth(n, lvl=1):
    if not n.get('children'):
        return lvl
    return max(depth(ch, lvl+1) for ch in n['children'])

print(f'Total nodes: {count(data)}')
print(f'Max depth: {depth(data)}')

# Show tree depth-3 children of first main dimension
print()
print('First main dim children:')
first = data['children'][0]
print(f'  {first["content"]}')
for ch in first.get('children', [])[:3]:
    print(f'    - {ch["content"]}')
    for ch2 in ch.get('children', [])[:3]:
        print(f'      - {ch2["content"]}')
        for ch3 in ch2.get('children', [])[:3]:
            print(f'        - {ch3["content"]}')