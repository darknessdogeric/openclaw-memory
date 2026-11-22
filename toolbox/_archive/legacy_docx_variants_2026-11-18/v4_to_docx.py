import docx, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# 读 v4.0 MD 内容
MD_PATH = r"D:/B166ER-OpenClaw/workspace/anyi-ops-kb/02_项目/高参峰会/邹士勇发言稿_2026高参圆桌国资酒店_2026-08-28_v4.0_精简版.md"
OUT_PATH = r"C:\Users\ericz\Desktop\邹士勇发言稿_2026高参圆桌国资酒店_2026-08-28_v4.0_精简版.docx"

with open(MD_PATH, encoding='utf-8') as f:
    content = f.read()

# 简单解析：分离正文与附
parts = content.split('## 附：v4.0 修订说明')
main_content = parts[0]
appendix = '## 附：v4.0 修订说明' + parts[1] if len(parts) > 1 else ''

# 创建 docx
doc = docx.Document()

# 设置默认字体（中文用宋体，西文用 Times New Roman）
style = doc.styles['Normal']
style.font.name = 'Times New Roman'
style.font.size = Pt(12)  # 小四号 ≈ 12pt
rpr = style.element.rPr
if rpr is None:
    rpr = OxmlElement('w:rPr')
    style.element.append(rpr)
rfonts = rpr.find(qn('w:rFonts'))
if rfonts is None:
    rfonts = OxmlElement('w:rFonts')
    rpr.append(rfonts)
rfonts.set(qn('w:eastAsia'), '宋体')

# 设置页面边距
for section in doc.sections:
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(3.17)
    section.right_margin = Cm(3.17)

# 标题信息
title_para = doc.add_paragraph()
title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
title_run = title_para.add_run('邹士勇发言稿 · 2026 酒店品牌展暨酒店投资峰会')
title_run.bold = True
title_run.font.size = Pt(16)  # 三号

subtitle = doc.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
sub_run = subtitle.add_run('（v4.0 · 精简版 · ≤4 页）')
sub_run.font.size = Pt(12)

# 元数据
info_lines = [
    ('会议', '2026 酒店品牌展暨酒店投资峰会'),
    ('环节', '高参圆桌——国资酒店的资产盘活与资本破局之道'),
    ('时间', '2026 年 9 月 1 日（周二）上午 11:20-12:10'),
    ('地点', '上海金茂君悦大酒店'),
    ('发言时长', '15 分钟'),
]
for label, value in info_lines:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(f'{label}: {value}')
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

doc.add_paragraph()  # 空行

# 解析 main_content 中的章节
def parse_md_to_docx(md_text, doc):
    lines = md_text.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if not line:
            i += 1
            continue

        # 一级标题（## 一、二、...）
        if line.startswith('## '):
            title_text = line[3:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(6)
            run = p.add_run(title_text)
            run.bold = True
            run.font.size = Pt(14)  # 小三号

        # 二级标题（### （一）/三、）
        elif line.startswith('### '):
            title_text = line[4:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(4)
            run = p.add_run(title_text)
            run.bold = True
            run.font.size = Pt(12)

        # 引用块（> ...）
        elif line.startswith('> '):
            quote_text = line[2:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.74)
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(4)
            run = p.add_run('　　' + quote_text)
            run.font.size = Pt(12)
            run.italic = True

        # 分隔线（---）
        elif line.strip() == '---':
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run('— · —— · ——')
            run.font.size = Pt(10)
            run.font.color.rgb = RGBColor(0x99, 0x99, 0x99)

        # 普通段落
        else:
            # 处理加粗标记 **xxx**
            import re
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = 1.5
            # 拆分 **xxx**
            parts = re.split(r'(\*\*[^*]+\*\*)', line)
            for part in parts:
                if not part:
                    continue
                if part.startswith('**') and part.endswith('**'):
                    run = p.add_run(part[2:-2])
                    run.bold = True
                else:
                    run = p.add_run(part)
                run.font.size = Pt(12)
        i += 1

# 解析主内容（跳过 # 标题和 ## ⚠️ 表格）
main_lines = []
skip_until = False
for line in main_content.split('\n'):
    if line.startswith('# '):
        continue
    if line.startswith('## ⚠️ v4.0'):
        skip_until = True
        continue
    if skip_until and line.startswith('---'):
        skip_until = False
        continue
    if skip_until:
        continue
    main_lines.append(line)
main_clean = '\n'.join(main_lines)

# 移除开头的元数据段（直到 "各位嘉宾"）
import re
match = re.search(r'各位嘉宾、各位同仁：', main_clean)
if match:
    main_clean = main_clean[match.start():]

# 写入主内容
parse_md_to_docx(main_clean, doc)

# 分页
doc.add_page_break()

# 附部分
if appendix:
    p = doc.add_paragraph()
    run = p.add_run('附：v4.0 修订说明（仅供内部查阅）')
    run.bold = True
    run.font.size = Pt(14)

    # 简化附内容
    appendix_clean = appendix.replace('## 附：v4.0 修订说明', '').replace('### ',', ')
    appendix_clean = appendix_clean.replace('## ', '')

    for line in appendix_clean.split('\n'):
        line = line.rstrip()
        if not line:
            continue
        if line.strip() == '---':
            continue
        if line.startswith('|') or '|' in line:
            # 表格行简化
            if not re.search(r'[一-龥]', line):
                continue  # 跳过分隔行
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(line.replace('|', ' | ').strip())
            run.font.size = Pt(9)
            run.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
        else:
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(2)
            import re as re2
            parts = re2.split(r'(\*\*[^*]+\*\*)', line)
            for part in parts:
                if not part:
                    continue
                if part.startswith('**') and part.endswith('**'):
                    run = p.add_run(part[2:-2])
                    run.bold = True
                else:
                    run = p.add_run(part)
                run.font.size = Pt(10)
                run.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

# 保存
doc.save(OUT_PATH)
print(f'✅ Saved: {OUT_PATH}')

# 统计
import os
size_kb = os.path.getsize(OUT_PATH) / 1024
print(f'   File size: {size_kb:.1f} KB')

# 字数
from docx import Document as Doc2
doc2 = Doc2(OUT_PATH)
total_chars = sum(len(p.text) for p in doc2.paragraphs)
zh_chars = sum(len(re.findall(r'[\u4e00-\u9fff]', p.text)) for p in doc2.paragraphs)
print(f'   Total chars: {total_chars}, Chinese chars: {zh_chars}')
print(f'   Paragraphs: {len(doc2.paragraphs)}')
pages_estimate = zh_chars / 800
pages_estimate_min = zh_chars / 850
pages_estimate_max = zh_chars / 750
print(f'   Estimated pages: {pages_estimate_min:.1f} - {pages_estimate_max:.1f}')
if zh_chars > 2550:
    print('   [WARN] > 3 pages, need further trimming')
elif zh_chars < 1800:
    print('   [WARN] < 2 pages, may look sparse')
print('   [DONE]')