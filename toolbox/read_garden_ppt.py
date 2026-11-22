"""读取花园宾馆改造 PPT 所有文本"""
from pptx import Presentation

p = Presentation(r'C:\Users\ericz\Desktop\产业发展部\花园宾馆改造\安逸·花园宾馆改造项目立项汇报（产业发展部）.pptx')
all_text = []
for i, slide in enumerate(p.slides, 1):
    slide_text = [f'\n=== Slide {i} ===']
    for shape in slide.shapes:
        if shape.has_text_frame:
            for para in shape.text_frame.paragraphs:
                text = para.text.strip()
                if text:
                    slide_text.append(text)
    all_text.append('\n'.join(slide_text))

content = '\n'.join(all_text)
with open(r'D:\B166ER-OpenClaw\workspace\toolbox\garden_ppt.txt', 'w', encoding='utf-8') as f:
    f.write(content)
print(f'已提取 {len(all_text)} 张 slide')
print(f'总字数: {len(content)}')