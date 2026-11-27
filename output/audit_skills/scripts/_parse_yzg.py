import fitz, os
f = r'C:\Users\ericz\Desktop\产业发展部\项目\安逸酒店集团数字化经营平台汇报V2.pdf'
doc = fitz.open(f)
out = [f'=== 安逸酒店集团数字化经营平台汇报 V2 ===', f'pages: {doc.page_count}', '']
for i, p in enumerate(doc, 1):
    out.append(f'=== Page {i} ===')
    out.append(p.get_text() or '(empty)')
    out.append('')
doc.close()
target = r'D:\B166ER-OpenClaw\workspace\memory\_parsed_yzg.txt'
with open(target, 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
print(f'wrote: {target} ({len(out)} lines)')