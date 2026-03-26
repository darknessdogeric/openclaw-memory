with open('C:/Users/ericz/.openclaw/workspace/memory/hotel-industry-knowledge-base.md', 'r', encoding='utf-8') as f:
    content = f.read()

marker = 'GMV目标:'
idx = content.find(marker)
if idx > 0:
    after = content[idx:]
    dash_idx = after.find('\n---')
    if dash_idx >= 0:
        section_idx = after.find('## 4.7.5')
        if section_idx >= 0:
            insert_point = idx + dash_idx + 1
            # Write surrounding content to file
            with open('C:/Users/ericz/.openclaw/workspace/insert_point.txt', 'w', encoding='utf-8') as out:
                out.write(f'Insert point char index: {insert_point}\n')
                out.write(f'Marker at: {idx}\n')
                out.write(f'Dash offset from marker: {dash_idx}\n')
                out.write(f'Section offset from marker: {section_idx}\n')
                out.write(f'Content at insert point:\n')
                out.write(repr(content[insert_point-30:insert_point+100]))
            print('Done, written to insert_point.txt')
