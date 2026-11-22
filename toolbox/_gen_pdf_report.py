# -*- coding: utf-8 -*-
"""
2026年6月经济数据报告 - PDF生成器 v2
使用 reportlab + 中文字体
"""
import os, re, sys
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FONT_DIR = r'C:\WINDOWS\Fonts'
pdfmetrics.registerFont(TTFont('STSong', os.path.join(FONT_DIR, 'STSONG.ttf')))
pdfmetrics.registerFont(TTFont('SimHei', os.path.join(FONT_DIR, 'simhei.ttf')))
pdfmetrics.registerFont(TTFont('SimSun', os.path.join(FONT_DIR, 'simsun.ttc'), subfontIndex=0))
pdfmetrics.registerFont(TTFont('MsYh', os.path.join(FONT_DIR, 'msyh.ttc'), subfontIndex=0))

DARK_NAVY = colors.HexColor('#1C2B3A')
ACCENT_BLUE = colors.HexColor('#2D5F8A')
LIGHT_GRAY = colors.HexColor('#F5F5F5')
MID_GRAY = colors.HexColor('#E0E0E0')
TEXT_DARK = colors.HexColor('#1A1A1A')

PAGE_W, PAGE_H = A4
MARGIN = 1.8 * cm
CONTENT_W = PAGE_W - 2 * MARGIN

styles = getSampleStyleSheet()

def S(name, **kw):
    """创建 ParagraphStyle 的简写"""
    base = kw.pop('parent', 'Normal')
    return ParagraphStyle(name, parent=styles[base], **kw)

TITLE_S   = S('T', fontName='SimHei', fontSize=28, leading=36, textColor=colors.white, alignment=TA_CENTER)
SUB_S    = S('Sub', fontName='MsYh', fontSize=14, leading=20, textColor=colors.HexColor('#CCDDEE'), alignment=TA_CENTER)
META_S   = S('Meta', fontName='MsYh', fontSize=9, leading=13, textColor=colors.HexColor('#8899AA'), alignment=TA_CENTER)
H1_S     = S('H1', fontName='SimHei', fontSize=15, leading=22, textColor=DARK_NAVY, spaceBefore=14, spaceAfter=6)
H2_S     = S('H2', fontName='SimHei', fontSize=12, leading=17, textColor=ACCENT_BLUE, spaceBefore=10, spaceAfter=5)
H3_S     = S('H3', fontName='MsYh', fontSize=10, leading=14, textColor=TEXT_DARK, spaceBefore=8, spaceAfter=3)
BODY_S    = S('Body', fontName='MsYh', fontSize=9, leading=13, textColor=TEXT_DARK, alignment=TA_JUSTIFY, spaceAfter=3)
TH_S     = S('TH', fontName='SimHei', fontSize=8, leading=11, textColor=colors.white, alignment=TA_CENTER)
TC_S     = S('TC', fontName='MsYh', fontSize=7.5, leading=10, textColor=TEXT_DARK)


def cover_page():
    """生成封面 flowables"""
    elems = []
    rows = [
        [Paragraph('', TITLE_S)],
        [Paragraph('', TITLE_S)],
        [Paragraph('', TITLE_S)],
        [Paragraph('2026年6月 / 上半年', TITLE_S)],
        [Paragraph('经济数据全方位解读', TITLE_S)],
        [Paragraph('', SUB_S)],
        [Paragraph('B166ER 出品 · 官方原文验证版', SUB_S)],
        [Paragraph('', META_S)],
        [Paragraph('', META_S)],
        [Paragraph('2026-07-15', META_S)],
        [Paragraph('', META_S)],
        [Paragraph('目标读者：Eric + 自留档', META_S)],
        [Paragraph('阅读时间：15-20分钟', META_S)],
        [Paragraph('', META_S)],
        [Paragraph('核心结论：房地产断崖 / 消费降级固化 / 高技术独苗', META_S)],
    ]
    t = Table(rows, colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), DARK_NAVY),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    elems.append(t)
    elems.append(PageBreak())
    return elems


def render_table(header, data_rows):
    """渲染 markdown 表格为 reportlab Table"""
    n = len(header)
    col_w = CONTENT_W / n
    tdata = [[Paragraph(h, TH_S) for h in header]]
    for row in data_rows:
        tdata.append([Paragraph(str(c).strip(), TC_S) for c in row])
    tbl = Table(tdata, colWidths=[col_w]*n, repeatRows=1)
    ts = [
        ('BACKGROUND', (0,0), (-1,0), ACCENT_BLUE),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'SimHei'),
        ('FONTSIZE', (0,0), (-1,0), 8),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('FONTNAME', (0,1), (-1,-1), 'MsYh'),
        ('FONTSIZE', (0,1), (-1,-1), 7.5),
        ('GRID', (0,0), (-1,-1), 0.3, MID_GRAY),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]
    for ri in range(1, len(tdata)):
        if ri % 2 == 0:
            ts.append(('BACKGROUND', (0,ri), (-1,ri), LIGHT_GRAY))
    tbl.setStyle(TableStyle(ts))
    return tbl


def parse_md_file(filepath):
    """解析 md，返回 (elements, table_objs)"""
    lines = Path(filepath).read_text(encoding='utf-8').split('\n')
    elems = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i].strip()

        # 跳过 frontmatter
        if i == 0 and line in ('---', '...'):
            while i < n and lines[i].strip() not in ('---', '...'):
                i += 1
            i += 1
            continue

        # 空行
        if not line:
            elems.append(Spacer(1, 4))
            i += 1
            continue

        # 阅读说明块
        if '阅读说明' in line and i > 0 and i < 5:
            elems.append(Paragraph('阅读说明', H2_S))
            j = i + 1
            while j < n and lines[j].strip().startswith('-'):
                bullet = lines[j].strip().lstrip('-* ').strip()
                if bullet:
                    elems.append(Paragraph(f'\u2022 {bullet}', BODY_S))
                j += 1
            elems.append(Spacer(1, 8))
            elems.append(HRFlowable(width='100%', thickness=1, color=ACCENT_BLUE, spaceAfter=8))
            i = j
            continue

        # 一级标题
        if line.startswith('## '):
            title = line[3:].strip()
            elems.append(Spacer(1, 6))
            elems.append(Paragraph(title, H1_S))
            elems.append(HRFlowable(width='100%', thickness=0.5, color=ACCENT_BLUE, spaceAfter=4))
            i += 1
            continue

        # 二级标题
        if line.startswith('### '):
            title = line[4:].strip()
            elems.append(Paragraph(title, H2_S))
            i += 1
            continue

        # 三级标题
        if line.startswith('#### '):
            title = line[5:].strip()
            elems.append(Paragraph(title, H3_S))
            i += 1
            continue

        # 分隔线
        if line in ('---', '***', '*****'):
            elems.append(Spacer(1, 6))
            elems.append(HRFlowable(width='100%', thickness=0.5, color=MID_GRAY, spaceAfter=4))
            i += 1
            continue

        # 表格：收集连续的所有 | 行
        if '|' in line and line.startswith('|'):
            # 收集整个表格
            tbl_lines = []
            j = i
            while j < n and '|' in lines[j] and lines[j].strip().startswith('|'):
                stripped = lines[j].strip()
                if stripped and not all(p.strip().startswith((':', '-')) for p in stripped.split('|')[1:-1] if p.strip()):
                    # 不是分隔行
                    pass
                # 收集所有行，后面过滤
                tbl_lines.append(stripped)
                j += 1

            # 提取表头（第一行）和数据行（跳过分隔行）
            if len(tbl_lines) >= 2:
                header = [p.strip() for p in tbl_lines[0].split('|')[1:-1]]
                data_rows = []
                for tl in tbl_lines[1:]:
                    parts = [p.strip() for p in tl.split('|')[1:-1]]
                    # 过滤掉分隔行
                    if parts and not all(re.match(r'^[:\- ]+$', p.replace(' ','')) for p in parts if p):
                        if len(parts) == len(header) or abs(len(parts) - len(header)) <= 2:
                            data_rows.append(parts)

                if header and data_rows:
                    elems.append(render_table(header, data_rows))
                    elems.append(Spacer(1, 5))
            i = j
            continue

        # 正文段落：处理 **bold** 和 *italic*
        clean = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', line)
        clean = re.sub(r'\*(.+?)\*', r'<i>\1</i>', clean)
        if clean.strip():
            elems.append(Paragraph(clean, BODY_S))
        i += 1

    return elems


def page_deco(canvas, doc):
    canvas.saveState()
    pg = canvas.getPageNumber()
    canvas.setFont('MsYh', 7.5)
    canvas.setFillColor(colors.HexColor('#888888'))
    canvas.drawCentredString(PAGE_W/2, 0.6*cm, f'B166ER 出品 · 2026年6月经济数据报告')
    canvas.drawRightString(PAGE_W - MARGIN, 0.6*cm, f'- {pg} -')
    if pg > 1:
        canvas.setStrokeColor(ACCENT_BLUE)
        canvas.setLineWidth(0.5)
        canvas.line(MARGIN, PAGE_H - 0.4*cm, PAGE_W - MARGIN, PAGE_H - 0.4*cm)
        canvas.setFillColor(colors.HexColor('#AAAAAA'))
        canvas.drawString(MARGIN, PAGE_H - 0.35*cm, '2026年6月经济数据报告')
    canvas.restoreState()


def main():
    md_path = Path(r'D:\B166ER-OpenClaw\workspace\reports\2026-07-15-6月经济数据全方位解读-PDF版.md')
    out_path = Path(r'D:\B166ER-OpenClaw\workspace\reports\pdf\2026-07-15-6月经济数据报告.pdf')
    out_path.parent.mkdir(parents=True, exist_ok=True)

    print('Parsing markdown...')
    elems = parse_md_file(md_path)
    print(f'Elements: {len(elems)}')

    # 封面
    cover = cover_page()

    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN + 0.5*cm,
        bottomMargin=1.2*cm,
        title='2026年6月/上半年经济数据全方位解读',
        author='B166ER',
    )

    all_elems = cover + elems
    doc.build(all_elems, onFirstPage=page_deco, onLaterPages=page_deco)
    size = out_path.stat().st_size
    print(f'PDF: {out_path}')
    print(f'Size: {size//1024} KB ({size//1024//1024} MB)')


if __name__ == '__main__':
    main()
