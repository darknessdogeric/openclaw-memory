with open('C:/Users/ericz/.openclaw/workspace/memory/hotel-industry-knowledge-base.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the insert point: after 私域月报模板 section, before ## 4.7.5 公域-私域营销闭环与新媒体矩阵
# The pattern is: GMV目标: ¥[Y]万\n```\n\n---\n\n## 4.7.5 公域-私域...

old_marker = '## 4.7.5 公域-私域营销闭环与新媒体矩阵'
idx = content.find(old_marker)
if idx < 0:
    print('ERROR: marker not found')
else:
    # Find the --- that precedes this section
    before = content[:idx]
    last_dash = before.rfind('\n---')
    if last_dash < 0:
        print('ERROR: --- not found')
    else:
        print(f'Found section at {idx}, --- at {last_dash}')
        print('Content around ---:')
        with open('C:/Users/ericz/.openclaw/workspace/ctx.txt', 'w', encoding='utf-8') as out:
            out.write(f'Section found at char {idx}\n')
            out.write(f'--- found at char {last_dash}\n')
            out.write('Around ---:\n')
            out.write(repr(content[last_dash-100:idx+200]))
        print('Done')
