with open('C:/Users/ericz/.openclaw/workspace/MEMORY.md', 'r', encoding='utf-8') as f:
    content = f.read()
for keyword in ['四川远途', '远途', '酒店业', '24年']:
    idx = content.find(keyword)
    if idx > 0:
        print(f'Found "{keyword}" at {idx}')
        print(content[idx:idx+200])
        print('---')
