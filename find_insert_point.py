with open('C:/Users/ericz/.openclaw/workspace/memory/hotel-industry-knowledge-base.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Find 私域月报模板 section end
marker = 'GMV目标:'
idx = content.find(marker)
if idx > 0:
    # Find the --- after this
    after = content[idx:]
    dash_idx = after.find('\n---')
    if dash_idx >= 0:
        # Find the ## 4.7.5
        section_idx = after.find('## 4.7.5')
        if section_idx >= 0:
            insert_point = idx + dash_idx + 1
            section_point = idx + section_idx
            print(f'Found marker at {idx}')
            print(f'Found --- at offset {dash_idx} from marker')
            print(f'Found ## 4.7.5 at offset {section_idx} from marker')
            print(f'Content around insert point:')
            print(repr(content[insert_point-50:insert_point+50]))
