import fitz, os
f = r'C:\Users\ericz\Desktop\产业发展部\项目\安逸酒店集团数字化经营平台汇报V2.pdf'
doc = fitz.open(f)
print(f'pages: {doc.page_count}, size: {os.path.getsize(f)} bytes')
for i, p in enumerate(doc):
    t = p.get_text()
    print(f'-- p{i+1} text_len={len(t)} imgs={len(p.get_images(full=True))}')
    if t:
        print(f'   preview: {t[:200]!r}')
doc.close()