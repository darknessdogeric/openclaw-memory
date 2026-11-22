"""检查模板文档的字体/样式设置"""
from docx import Document

template = Document(r'C:\Users\ericz\Desktop\邹士勇总发言稿（2026酒店品牌展暨酒店投资峰会）.docx')
print('=== 模板文档样式信息 ===')
print(f'段落数: {len(template.paragraphs)}')
print(f'表格数: {len(template.tables)}')
print()

normal = template.styles['Normal']
print(f'Normal 字体: {normal.font.name}')
print(f'Normal 字号: {normal.font.size}')
print()

for level in range(1, 4):
    try:
        h = template.styles[f'Heading {level}']
        print(f'Heading {level}: 字体={h.font.name}, 字号={h.font.size}')
    except KeyError:
        print(f'Heading {level}: 不存在')

print()
print('=== 检查前 3 个正文字体设置 ===')
for i, p in enumerate(template.paragraphs[:5]):
    if p.text.strip():
        for run in p.runs[:1]:
            print(f'P{i}: 字体={run.font.name}, 字号={run.font.size}, 粗体={run.bold}')
            rpr = run._element.rPr
            if rpr is not None:
                rfonts = rpr.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rFonts')
                if rfonts is not None:
                    print(f'  eastAsia: {rfonts.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}eastAsia")}')
                    print(f'  ascii: {rfonts.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}ascii")}')
