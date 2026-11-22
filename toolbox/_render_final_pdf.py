# -*- coding: utf-8 -*-
"""B166ER: 用 reportlab 把综合报告渲染成 PDF"""
import os, sys
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FONT_DIR = r'C:\WINDOWS\Fonts'
pdfmetrics.registerFont(TTFont('SimHei', os.path.join(FONT_DIR, 'simhei.ttf')))
pdfmetrics.registerFont(TTFont('SimSun', os.path.join(FONT_DIR, 'simsun.ttc'), subfontIndex=0))
pdfmetrics.registerFont(TTFont('MsYh', os.path.join(FONT_DIR, 'msyh.ttc'), subfontIndex=0))

DARK_NAVY = colors.HexColor('#1C2B3A')
ACCENT_BLUE = colors.HexColor('#2D5F8A')
ACCENT_ORANGE = colors.HexColor('#D97706')
LIGHT_GRAY = colors.HexColor('#F5F5F5')
MID_GRAY = colors.HexColor('#E0E0E0')
TEXT_DARK = colors.HexColor('#1A1A1A')
LIGHT_BLUE_BG = colors.HexColor('#E8F0F8')

PAGE_W, PAGE_H = A4
MARGIN = 1.8 * cm
CONTENT_W = PAGE_W - 2 * MARGIN

styles = getSampleStyleSheet()
def S(name, **kw):
    base = kw.pop('parent', 'Normal')
    return ParagraphStyle(name, parent=styles[base], **kw)

TITLE_S   = S('T', fontName='SimHei', fontSize=22, leading=28, textColor=colors.white, alignment=TA_CENTER)
SUB_S    = S('Sub', fontName='MsYh', fontSize=13, leading=18, textColor=colors.HexColor('#CCDDEE'), alignment=TA_CENTER)
META_S   = S('Meta', fontName='MsYh', fontSize=9, leading=13, textColor=colors.HexColor('#8899AA'), alignment=TA_CENTER)
H1_S     = S('H1', fontName='SimHei', fontSize=16, leading=22, textColor=DARK_NAVY, spaceBefore=14, spaceAfter=8)
H2_S     = S('H2', fontName='SimHei', fontSize=12.5, leading=17, textColor=ACCENT_BLUE, spaceBefore=10, spaceAfter=5)
H3_S     = S('H3', fontName='SimHei', fontSize=11, leading=15, textColor=ACCENT_ORANGE, spaceBefore=8, spaceAfter=3)
H4_S     = S('H4', fontName='MsYh', fontSize=10, leading=14, textColor=ACCENT_BLUE, spaceBefore=6, spaceAfter=3)
BODY_S    = S('Body', fontName='MsYh', fontSize=9, leading=13.5, textColor=TEXT_DARK, alignment=TA_JUSTIFY, spaceAfter=4)
TH_S     = S('TH', fontName='SimHei', fontSize=8.5, leading=11, textColor=colors.white, alignment=TA_CENTER)
TC_S     = S('TC', fontName='MsYh', fontSize=8, leading=11, textColor=TEXT_DARK)
TC_CT_S  = S('TCC', fontName='MsYh', fontSize=8, leading=11, textColor=TEXT_DARK, alignment=TA_CENTER)
QUOTE_S  = S('Q', fontName='MsYh', fontSize=9.5, leading=15, textColor=DARK_NAVY,
              leftIndent=14, rightIndent=14, spaceBefore=5, spaceAfter=5,
              borderColor=ACCENT_BLUE, borderWidth=0, borderPad=4, backColor=LIGHT_BLUE_BG)
EMPH_S   = S('E', fontName='SimHei', fontSize=9.5, leading=14, textColor=DARK_NAVY)

# ============ Cover ============
def cover():
    rows = [
        [Paragraph('', TITLE_S)],
        [Paragraph('2026.07.16', META_S)],
        [Paragraph('', META_S)],
        [Paragraph('新能源车外挂小蓝灯', TITLE_S)],
        [Paragraph('从现象到本质', TITLE_S)],
        [Paragraph('', SUB_S)],
        [Paragraph('综合研究报告 / Phase 2+3 完整产物', SUB_S)],
        [Paragraph('', META_S)],
        [Paragraph('', META_S)],
        [Paragraph('由 B166ER 主会话综合', META_S)],
        [Paragraph('基于 6 份 sub-agent 子报告 + DeepSeek 综合推理', META_S)],
        [Paragraph('', META_S)],
        [Paragraph('', META_S)],
        [Paragraph('核心结论：', META_S)],
        [Paragraph('小蓝灯不是灯，是 AI 时代', TITLE_S)],
        [Paragraph('中国中产身份焦虑的商品化', TITLE_S)],
        [Paragraph('', META_S)],
        [Paragraph('', META_S)],
        [Paragraph('阅读时间：约 30 分钟', META_S)],
        [Paragraph('总数据：163 KB / 102 次搜索 / 14 详情页', META_S)],
        [Paragraph('Eric 12:26 指令 - 综合分析', META_S)],
    ]
    t = Table(rows, colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), DARK_NAVY),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    return [t, PageBreak()]

# ============ Renderer ============
def render_table(header, data_rows, col_widths=None):
    n = len(header)
    if col_widths is None:
        col_widths = [CONTENT_W / n] * n
    tdata = [[Paragraph(h, TH_S) for h in header]]
    for row in data_rows:
        cells = []
        for c in row:
            cells.append(Paragraph(str(c).strip(), TC_S))
        tdata.append(cells)
    tbl = Table(tdata, colWidths=col_widths, repeatRows=1)
    ts = [
        ('BACKGROUND', (0,0), (-1,0), ACCENT_BLUE),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('FONTNAME', (0,1), (-1,-1), 'MsYh'),
        ('GRID', (0,0), (-1,-1), 0.3, MID_GRAY),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]
    for ri in range(1, len(tdata)):
        if ri % 2 == 0:
            ts.append(('BACKGROUND', (0,ri), (-1,ri), LIGHT_GRAY))
    tbl.setStyle(TableStyle(ts))
    return tbl

def clean_md(text):
    """Clean inline markdown"""
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    text = re.sub(r'`(.+?)`', r'<font name="SimHei">\1</font>', text)
    return text

import re

def parse_md(filepath):
    lines = Path(filepath).read_text(encoding='utf-8').split('\n')
    elems = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i].strip()

        if i == 0 and line in ('---', '...'):
            while i < n and lines[i].strip() not in ('---', '...'):
                i += 1
            i += 1
            continue

        if not line:
            elems.append(Spacer(1, 4))
            i += 1
            continue

        # 一级标题 #
        if line.startswith('# ') and not line.startswith('## '):
            title = line[2:].strip()
            elems.append(Paragraph(title, H1_S))
            elems.append(HRFlowable(width='100%', thickness=0.6, color=ACCENT_BLUE, spaceAfter=4))
            i += 1
            continue

        # 二级标题 ##
        if line.startswith('## '):
            title = line[3:].strip()
            elems.append(Spacer(1, 6))
            elems.append(Paragraph(title, H2_S))
            elems.append(HRFlowable(width='100%', thickness=0.4, color=MID_GRAY, spaceAfter=3))
            i += 1
            continue

        # 三级标题 ###
        if line.startswith('### '):
            title = line[4:].strip()
            elems.append(Paragraph(title, H3_S))
            i += 1
            continue

        # 四级标题 ####
        if line.startswith('#### '):
            title = line[5:].strip()
            elems.append(Paragraph(title, H4_S))
            i += 1
            continue

        # 分隔线
        if line in ('---', '***', '*****'):
            elems.append(HRFlowable(width='100%', thickness=0.4, color=MID_GRAY, spaceAfter=4))
            i += 1
            continue

        # 表格
        if '|' in line and line.startswith('|'):
            tbl_lines = []
            j = i
            while j < n and '|' in lines[j] and lines[j].strip().startswith('|'):
                tbl_lines.append(lines[j].strip())
                j += 1

            header = []
            data_rows = []
            if len(tbl_lines) >= 2:
                header = [p.strip() for p in tbl_lines[0].split('|')[1:-1]]
                for tl in tbl_lines[1:]:
                    parts = [p.strip() for p in tl.split('|')[1:-1]]
                    if parts and not all(re.match(r'^[:\- ]+$', p.replace(' ','')) for p in parts if p):
                        if len(parts) == len(header) or abs(len(parts) - len(header)) <= 2:
                            data_rows.append(parts)

            if header and data_rows:
                n_cols = len(header)
                col_widths = [CONTENT_W / n_cols] * n_cols
                elems.append(render_table(header, data_rows, col_widths))
                elems.append(Spacer(1, 5))
            i = j
            continue

        # 引用 >
        if line.startswith('>'):
            content = line[1:].strip()
            content = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', content)
            elems.append(Paragraph(content, QUOTE_S))
            i += 1
            continue

        # 代码块 ```
        if line.startswith('```'):
            i += 1
            code_lines = []
            while i < n and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            i += 1
            if code_lines:
                code_text = '<br/>'.join(code_lines)
                code_style = ParagraphStyle('Code', parent=styles['Code'],
                    fontName='SimHei', fontSize=8, leading=11,
                    textColor=TEXT_DARK, backColor=LIGHT_GRAY,
                    leftIndent=8, rightIndent=8, spaceBefore=4, spaceAfter=4)
                elems.append(Paragraph(code_text, code_style))
            continue

        # bullet point
        if line.startswith('- '):
            content = line[2:].strip()
            content = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', content)
            elems.append(Paragraph(f'• {content}', BODY_S))
            i += 1
            continue

        # 普通段落
        clean = clean_md(line)
        if clean.strip():
            elems.append(Paragraph(clean, BODY_S))
        i += 1

    return elems


def page_deco(canvas, doc):
    canvas.saveState()
    pg = canvas.getPageNumber()
    canvas.setFont('MsYh', 7.5)
    canvas.setFillColor(colors.HexColor('#888888'))
    canvas.drawCentredString(PAGE_W/2, 0.6*cm, 'B166ER 出品 · 新能源车外挂小蓝灯 · 从现象到本质')
    canvas.drawRightString(PAGE_W - MARGIN, 0.6*cm, f'- {pg} -')
    if pg > 1:
        canvas.setStrokeColor(ACCENT_BLUE)
        canvas.setLineWidth(0.5)
        canvas.line(MARGIN, PAGE_H - 0.4*cm, PAGE_W - MARGIN, PAGE_H - 0.4*cm)
    canvas.restoreState()


def main():
    md_path = Path(r'D:\B166ER-OpenClaw\workspace\reports\2026-07-16-新能源车外挂小蓝灯-从现象到本质-综合报告.md')
    out_path = Path(r'D:\B166ER-OpenClaw\workspace\reports\pdf\2026-07-16-新能源车外挂小蓝灯-综合报告.pdf')
    out_path.parent.mkdir(parents=True, exist_ok=True)

    print('Parsing...')
    elems = parse_md(md_path)
    print(f'Elements: {len(elems)}')

    cover_elems = cover()
    all_elems = cover_elems + elems

    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN + 0.5*cm,
        bottomMargin=1.2*cm,
        title='新能源车外挂小蓝灯 - 从现象到本质',
        author='B166ER',
    )

    doc.build(all_elems, onFirstPage=page_deco, onLaterPages=page_deco)

    size_kb = out_path.stat().st_size // 1024
    print(f'\nPDF: {out_path}')
    print(f'Size: {size_kb} KB')

    # 复制到桌面
    import shutil
    desktop = Path(r'C:\Users\ericz\Desktop\2026-07-16-新能源车外挂小蓝灯-综合报告.pdf')
    shutil.copy(str(out_path), str(desktop))
    print(f'Desktop: {desktop}')


if __name__ == '__main__':
    main()
