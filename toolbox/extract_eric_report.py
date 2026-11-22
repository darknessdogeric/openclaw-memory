import fitz
doc = fitz.open(r'C:\Users\ericz\Desktop\产业发展部\给董事长的单独汇报\安逸集团改革发展与三大核心竞争力综合报告_v1.1.pdf')
with open(r'D:\B166ER-OpenClaw\workspace\toolbox\eric_report.txt', 'w', encoding='utf-8') as f:
    for i in range(doc.page_count):
        page = doc[i]
        text = page.get_text()
        f.write(f'=== Page {i+1} ===\n')
        f.write(text)
        f.write('\n\n')
doc.close()
print('done')
