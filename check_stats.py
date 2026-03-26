with open('C:/Users/ericz/.openclaw/workspace/memory/hotel-industry-knowledge-base.md', 'r', encoding='utf-8') as f:
    content = f.read()
print(f'Chars: {len(content)}')
print(f'Lines: {content.count(chr(10))}')
idx = content.find('## 4.9')
print(f'4.9 section found at character: {idx}')
