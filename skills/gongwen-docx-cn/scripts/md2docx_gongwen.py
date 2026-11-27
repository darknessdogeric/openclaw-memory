"""
公文格式 Markdown → Word（GB/T 9704-2012 合规 + Eric 排版习惯）
合并两套脚本：公文编号规则 + 通用表格/列表/代码块支持

字体规范（GB/T 9704-2012《党政机关公文格式》）:
  标题        方正小标宋简体 二号（22pt）
  正文        仿宋_GB2312        三号（16pt）
  一级标题(一、) 黑体          三号（16pt）
  二级标题((一)) 楷体_GB2312    三号（16pt）
  三级标题(1.)  楷体_GB2312    三号（16pt）

排版规范:
  - 行距 固定值 28-30 磅
  - 首行缩进 2 字符（403225 EMU）
  - 页边距 上下 2.54cm，左右 3.18cm
  - 表格：黑色 0.5pt 单线边框，表头加粗
  - 代码块：缩进 2 字符，11pt，行距 1.15
  - 引用：左缩进 2 字符
  - 列表：纯文字无项目符号（用序号或换行）
  - 无 emoji / 无符号装饰 / 无元数据章节
"""
import sys, io, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from docx import Document
from docx.shared import Pt, Cm, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# 字体（GB/T 9704-2012）
TITLE_FONT = '方正小标宋简体'    # 标题
BODY_FONT   = '仿宋_GB2312'      # 正文（GB/T 9704 标准仿宋，非泛指“仿宋”）
EN_FONT     = 'Times New Roman'  # 西文与数字
H1_FONT     = '黑体'              # 一级标题
H2_FONT     = '楷体'              # 二级标题

# 缩进与间距（EMU，1磅=12700）
IND = Emu(403225)                   # 2 字符首行缩进
H1_SB, H1_SA = Emu(152400), Emu(76200)   # 一级：段前12磅 段后6磅
H2_SB, H2_SA = Emu(101600), Emu(50800)   # 二级：段前8磅 段后4磅
LS_EXACT = Pt(28)                  # 行距：固定 28 磅（GB/T 9704；2026-11-17 补：脚本原先不设行距）

if len(sys.argv) < 3:
    print('用法: python md2docx_gongwen.py <src.md> <dst.docx>')
    sys.exit(1)
SRC, DST = sys.argv[1], sys.argv[2]


def set_font(run, name, size):
    """绑定中英文字体（必须设 eastAsia 才能正确显示中文）"""
    run.font.size = Pt(size)
    run.font.name = name
    rpr = run._element.get_or_add_rPr()
    rf = rpr.find(qn('w:rFonts'))
    if rf is None:
        rf = OxmlElement('w:rFonts')
        rpr.append(rf)
    # 关键：eastAsia 决定中文/西文字符使用哪个字体
    rf.set(qn('w:eastAsia'), name)
    rf.set(qn('w:ascii'), EN_FONT)      # 西文/数字必须 Times New Roman，否则数字按中文字体渲染会变形
    rf.set(qn('w:hAnsi'), EN_FONT)
    rf.set(qn('w:cs'), EN_FONT)


def add_para(doc, text, font=BODY_FONT, size=16,
             align=None, indent=True, sa=None, sb=None,
             bold=False, line_spacing=None):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    if align is not None:
        p.alignment = align
    if indent:
        pf.first_line_indent = IND
    if sa is not None:
        pf.space_after = sa
    if sb is not None:
        pf.space_before = sb
    # 行距：默认固定 28 磅（标题/正文/各级标题统一；代码块另设 1.15）
    pf.line_spacing = LS_EXACT if line_spacing is None else line_spacing
    run = p.add_run(text)
    run.bold = bold
    set_font(run, font, size)
    return p


def add_title(doc, text):
    """公文标题：方正小标宋简体 二号 居中。文本中的“｜”表示手动换行（长标题按公文习惯折行居中）"""
    p = doc.add_paragraph()
    pf = p.paragraph_format
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf.space_after = Emu(254000)
    pf.line_spacing = LS_EXACT
    parts = [x for x in text.split('｜') if x.strip()]
    for i, seg in enumerate(parts):
        run = p.add_run(seg)
        set_font(run, TITLE_FONT, 22)
        if i < len(parts) - 1:
            run.add_break()
    return p


def add_table(doc, rows, size=11):
    """GB/T 9704 风格表格：黑色边框、表头加粗、单元格内左对齐"""
    if not rows:
        return None
    ncol = len(rows[0])          # 以表头列宽为准（2026-11-21 加固：数据行多列会撑出空列）
    t = doc.add_table(rows=0, cols=ncol)
    t.style = 'Table Grid'
    for ri, row in enumerate(rows):
        cells = t.add_row().cells
        for i, val in enumerate(row):
            if i < len(cells):
                cells[i].text = ''
                run = cells[i].paragraphs[0].add_run(str(val))
                run.bold = (ri == 0)  # 表头加粗
                set_font(run, BODY_FONT, size)
    P(doc, '')  # 表格后空行
    return t


def P(doc, text='', size=10, sa=Emu(50800)):
    """小空行"""
    if text:
        add_para(doc, text, font=BODY_FONT, size=size, sa=sa)
    else:
        add_para(doc, ' ', font=BODY_FONT, size=10, indent=False, sa=sa)


def add_code_block(doc, lines, size=11):
    """代码块：缩进 2 字符 + 1.15 行距 + 等宽感"""
    for b in lines:
        if not b.strip():
            continue
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.left_indent = IND
        pf.space_after = Emu(12700)
        pf.line_spacing = 1.15
        run = p.add_run(b)
        set_font(run, BODY_FONT, size)


# 标题识别
RE_TITLE = re.compile(r'^(.{2,})$')           # 第一行（标题）
RE_H1    = re.compile(r'^[一二三四五六七八九十]+、')   # 一、（公文）
RE_H2    = re.compile(r'^（[一二三四五六七八九十]+）')    # （一）（公文）
RE_H3    = re.compile(r'^\d+\.\s')                # 1. （三级）
RE_HR    = '---'                                 # 分隔线
RE_TABLE = re.compile(r'^\|.*\|$')                # 表格行
RE_CODE  = re.compile(r'^```')                   # 代码块

# 抬头识别（呈：xxx / 拟：xxx / 时间：xxx）
HEADER_PREFIXES = ('呈：', '拟：', '时间：', '呈:', '拟:', '时间:')

# 落款识别（2026-11-17 扩展：单位名后缀 + 任意年月日写法，避免落款被当正文左对齐）
SIGNOFF = ('产业发展部', '2026 年 9 月', '2026年9月')
RE_DATE = re.compile(r'^20\d{2}\s*年\s*\d{1,2}\s*月(\s*\d{1,2}\s*日)?$')


def is_signoff(s):
    if s in SIGNOFF:
        return True
    if s.endswith('发展部') or s.endswith('部'):          # 安逸酒店集团产业发展部 等
        return True
    if RE_DATE.match(s.replace(' ', '')) or RE_DATE.match(s):
        return True
    return False


def is_zhusong(s):
    """主送机关：短句且以冒号结尾，顶格不缩进"""
    return s.endswith('：') and len(s) <= 14 and not any(s.startswith(p) for p in HEADER_PREFIXES)


def md_to_gongwen_docx(src_md, dst_docx):
    with open(src_md, encoding='utf-8') as f:
        lines = [l.rstrip() for l in f.read().splitlines()]
    lines = [l for l in lines if l.strip()]  # 跳过纯空行（但保留表格内的空行）

    doc = Document()
    sec = doc.sections[0]
    # GB/T 9704 标准页边距
    sec.page_width = Cm(21.0)      # A4 宽（默认模板是 Letter 8.5in，必须显式设定）
    sec.page_height = Cm(29.7)     # A4 高
    sec.top_margin = Cm(3.7)
    sec.bottom_margin = Cm(3.5)
    sec.left_margin = Cm(2.8)
    sec.right_margin = Cm(2.6)

    i = 0
    n = len(lines)
    is_first = True

    while i < n:
        line = lines[i]
        s = line.strip()

        # 代码块（可包含空行）
        if RE_CODE.match(s):
            i += 1
            buf = []
            while i < n and not RE_CODE.match(lines[i].strip()):
                buf.append(lines[i])
                i += 1
            i += 1  # 跳过结尾 ```
            add_code_block(doc, buf)
            P(doc, '')  # 代码块后空行
            is_first = False
            continue

        # 表格（连续 | 行，含分隔行 |---|）
        if RE_TABLE.match(s):
            rows = []
            while i < n and RE_TABLE.match(lines[i].strip()):
                row = lines[i].strip()
                # 跳过表头分隔行（| --- | --- |）
                if re.match(r'^\|[\s\-:|]+\|$', row):
                    i += 1
                    continue
                cells = [c.strip() for c in row.strip('|').split('|')]
                rows.append(cells)
                i += 1
            add_table(doc, rows)
            is_first = False
            continue

        # 分隔线
        if s == RE_HR:
            P(doc, '')
            i += 1
            is_first = False
            continue

        # 引用
        if s.startswith('>'):
            txt = s.lstrip('> ').strip()
            p = doc.add_paragraph()
            pf = p.paragraph_format
            pf.left_indent = IND
            pf.space_after = Emu(25400)
            run = p.add_run(txt)
            set_font(run, BODY_FONT, 13)
            i += 1
            is_first = False
            continue

        # 第一行：标题（方正小标宋 二号 居中，“｜”处手动换行）
        if is_first:
            add_title(doc, s)
            is_first = False
            i += 1
            continue

        # 抬头：呈：xxx / 拟：xxx / 时间：xxx
        if any(s.startswith(p) for p in HEADER_PREFIXES):
            add_para(doc, s, font=BODY_FONT, size=16,
                     align=WD_ALIGN_PARAGRAPH.RIGHT, indent=False,
                     sa=Emu(25400))
            i += 1
            continue

        # 主送机关：顶格
        if is_zhusong(s):
            add_para(doc, s, font=BODY_FONT, size=16, indent=False, sa=Emu(25400))
            i += 1
            continue

        # 落款
        if is_signoff(s):
            add_para(doc, s, font=BODY_FONT, size=16,
                     align=WD_ALIGN_PARAGRAPH.RIGHT, indent=False)
            i += 1
            continue

        # 一级标题 一、（黑体三号）
        if RE_H1.match(s):
            add_para(doc, s, font=H1_FONT, size=16,
                     indent=True, sb=H1_SB, sa=H1_SA)
            i += 1
            continue

        # 二级标题 （一）（楷体三号）
        if RE_H2.match(s):
            # 二级标题加粗：对齐集团 AI-RMS 请示（2026-11-05）体例
            add_para(doc, s, font=H2_FONT, size=16, bold=True,
                     indent=True, sb=H2_SB, sa=H2_SA)
            i += 1
            continue

        # 三级标题 1. （楷体三号）
        if RE_H3.match(s):
            add_para(doc, s, font=H2_FONT, size=16,
                     indent=True, sb=H2_SB, sa=H2_SA)
            i += 1
            continue

        # 列表：纯文字（无项目符号，符合公文规范）
        #   - "- xxx" 或 "* xxx"  → 序号或换行
        #   - "数字. xxx"  → 三级标题（上面已处理）
        #   - 这里统一处理为带缩进的纯文字段落
        m = re.match(r'^[-*]\s+(.*)', s)
        if m:
            txt = m.group(1)
            # 去粗体（保留语义）
            txt = re.sub(r'\*\*(.+?)\*\*', r'\1', txt)
            add_para(doc, txt, font=BODY_FONT, size=15)
            i += 1
            continue

        # 普通正文
        txt = re.sub(r'\*\*(.+?)\*\*', r'\1', s)
        txt = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'\1', txt)
        txt = re.sub(r'`(.+?)`', r'\1', txt)
        add_para(doc, txt, font=BODY_FONT, size=16)
        i += 1

    doc.save(dst_docx)
    print(f'OK {os.path.getsize(dst_docx)} bytes -> {dst_docx}')


if __name__ == '__main__':
    md_to_gongwen_docx(SRC, DST)
